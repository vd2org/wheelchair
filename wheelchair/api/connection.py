# Copyright (C) 2019-2021 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import json
import logging
from typing import Optional, List, Dict, Union
from urllib.parse import urlsplit, urljoin, quote, urlencode

from aiohttp import ClientSession, ClientTimeout

from .auth import Auth, CookieAuth
from .cluster_setup import ClusterSetup
from .database import DatabaseProxy
from .exceptions import RequestError, UnauthorizedError
from .node import NodeProxy
from .scheduler import Scheduler
from .server import Server
from .session import Session
from .utils import Query
from .utils.query import StreamResponse, StreamRequest

default_logger = logging.getLogger('wheelchair')


class Connection:
    __asyncio_session: Optional[ClientSession] = None

    def __init__(self, scheme: str, hostname: str, port: int, auth: Auth, *,
                 logger: Optional[logging.Logger] = None):
        """

        :param scheme: Connection string to CouchDB
        :param hostname: Connection string to CouchDB
        :param port: Connection string to CouchDB
        :param auth: Authentication provider
        :param logger: Custom logger
        """

        self.__url = f"{scheme}://{hostname}:{port}/"
        self.__auth = auth

        self.__asyncio_session = ClientSession()
        self.__logger = logger or default_logger

    @classmethod
    def from_string(cls, connection_string: str, logger: Optional[logging.Logger] = None) -> 'Connection':
        p = urlsplit(connection_string)
        assert p.hostname, "Server should have hostname!"
        assert p.scheme in ('http', 'https'), "Scheme should be http or https"
        assert p.username, "Connection string should have username"
        assert p.password, "Connection string should have password"

        port = p.port

        if not port:
            if p.scheme == 'http':
                port = 5984
            else:  # https
                port = 443

        return cls(p.scheme, p.hostname, port, CookieAuth(p.username, p.password), logger=logger or default_logger)

    @classmethod
    def from_string_and_credentials(cls, connection_string: str, username: str, password: str,
                                    logger: Optional[logging.Logger] = None) -> 'Connection':
        p = urlsplit(connection_string)
        assert p.hostname, "Server should have hostname!"
        assert p.scheme in ('http', 'https'), "Scheme should be http or https"
        assert p.username is None, "Connection string shouldn't have username"
        assert p.password is None, "Connection string shouldn't have password"

        port = p.port

        if not port:
            if p.scheme == 'http':
                port = 5984
            else:  # https
                port = 443

        return cls(p.scheme, p.hostname, port, CookieAuth(username, password), logger=logger or default_logger)

    @classmethod
    def from_string_and_auth(cls, connection_string: str, auth: Auth,
                             logger: Optional[logging.Logger] = None) -> 'Connection':
        p = urlsplit(connection_string)
        assert p.hostname, "Server should have hostname!"
        assert p.scheme in ('http', 'https'), "Scheme should be http or https"
        assert p.username is None, "Connection string shouldn't have username"
        assert p.password is None, "Connection string shouldn't have password"

        port = p.port

        if not port:
            if p.scheme == 'http':
                port = 5984
            else:  # https
                port = 443

        return cls(p.scheme, p.hostname, port, auth, logger=logger or default_logger)

    @property
    def url(self) -> str:
        return self.__url

    async def direct_query(self, query: Query, as_stream: bool = False,
                           timeout: Optional[int] = None) -> Union[int, str, List, Dict, StreamResponse]:
        method, path, params, data, headers = await self.__auth(self, query)

        timeout = ClientTimeout(total=timeout)

        headers = headers if headers else {}

        if isinstance(data, StreamRequest):
            headers['Content-Type'] = data.content_type
        elif isinstance(data, dict):
            if data:
                data = {k: v for k, v in data.items() if v is not None}

            headers['Content-Type'] = 'application/json'

        else:  # isinstance(data, str) or isinstance(data, int) == True
            headers['Content-Type'] = 'application/json'

        path = "/".join([quote(i, safe='') for i in path if i is not None])

        if params:
            params = {k: self._format_query_param(v) for k, v in params.items() if v is not None}
            qs = urlencode(params)

            if qs:
                path = f"{path}?{qs}"

        full_url = urljoin(self.__url, path)

        self.__logger.debug("Querying CouchDB: %s %s", method, full_url)

        if isinstance(data, StreamRequest):
            req = await self.__asyncio_session.request(method, full_url, data=data.stream, headers=headers,
                                                       timeout=timeout)
        else:  # isinstance(data, dict) == True
            req = await self.__asyncio_session.request(method, full_url, json=data, headers=headers, timeout=timeout)

        if as_stream and req.status in (200, 201, 202):
            return StreamResponse(req.headers['Content-Type'], req.content)

        res = await req.json()

        if isinstance(res, dict) and 'error' in res:
            raise RequestError.get_exception(req.status, res)

        return res

    async def query(self, method: str,
                    path: List[str],
                    *,
                    params: Optional[dict] = None,
                    data: Optional[Union[int, str, dict, StreamRequest]] = None,
                    headers: Optional[dict] = None,
                    as_stream: bool = False,
                    timeout: Optional[int] = None) -> Union[int, str, List, Dict, StreamResponse]:
        """
        Performs request to CouchDB

        :param method: Request method
        :param path: Request path
        :param params: Query parameters
        :param data: Data
        :param headers: Request headers
        :param as_stream: Return StreamResponse instead of processed object
        :param timeout: Set custom timeout for logpool requests
        :return: Result of the request
        """

        query = Query(method, path, params, data, headers)

        try:
            return await self.direct_query(query, as_stream, timeout)
        except UnauthorizedError:
            pass

        # We are here because an UnauthorizedError occurred
        # Let's try authentication and try again to execute the request
        await self.authenticate()
        return await self.direct_query(query, as_stream, timeout)

    @property
    def server(self) -> Server:
        return Server(self)

    @property
    def cluster_setup(self) -> ClusterSetup:
        return ClusterSetup(self)

    @property
    def scheduler(self) -> Scheduler:
        return Scheduler(self)

    @property
    def node(self) -> NodeProxy:
        return NodeProxy(self)

    @property
    def session(self) -> Session:
        return Session(self)

    @property
    def db(self) -> DatabaseProxy:
        return DatabaseProxy(self)

    async def authenticate(self):
        """Performs authentication though given auth."""

        return await self.__auth.authenticate(self)

    async def shutdown_cleanup(self):
        if self.__asyncio_session is None:
            return

        s = self.__asyncio_session
        self.__asyncio_session = None
        await s.close()

    def __del__(self):
        if self.__asyncio_session:
            self.__logger.warning("Default session is not closed! "
                                  "You must call Connector.shutdown_cleanup() before exit!")

    @staticmethod
    def _format_query_param(v):
        if isinstance(v, (dict, list)):
            return json.dumps(v)
        if isinstance(v, bool):
            return "true" if v else "false"

        return str(v)
