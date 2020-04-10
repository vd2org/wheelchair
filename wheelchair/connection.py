# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import json
import logging
from typing import Optional, List, Dict, Union
from urllib.parse import urlsplit, urljoin, quote, urlencode

from aiohttp import ClientSession, ClientResponse

from .database import Database, DatabaseProxy
from .exceptions import RequestError, UnauthorizedError

default_logger = logging.getLogger('wheelchair.connection')


class Connection:
    __session: Optional[ClientSession] = None

    def __init__(self, server: str, *, logger: Optional[logging.Logger] = None):
        """

        :param server: Connection string to CouchDB
        :param logger: Custom logger
        """

        p = urlsplit(server)
        assert p.hostname, "Server should have hostname!"
        assert p.scheme in ('http', 'https'), "Scheme should be http or https"
        port = p.port if p.port else 5984

        self.__server = f"{p.scheme}://{p.hostname}:{port}/"
        self.__username = p.username
        self.__password = p.password

        self.__session = ClientSession()
        self.__logger = logger or default_logger

    @property
    def server(self) -> str:
        return self.__server

    async def _query(self, method: str,
                     path: List[str],
                     params: Optional[dict] = None,
                     data: Optional[dict] = None) -> Union[List, Dict, ClientResponse]:

        path = "/".join([quote(i, safe='') for i in path])

        if params:
            params = {k: self._format_query_param(v) for k, v in params.items() if v is not None}
            qs = urlencode(params)

            if qs:
                path = f"{path}?{qs}"

        full_url = urljoin(self.__server, path)

        self.__logger.debug("Querying CouchDB: %s %s", method, full_url)

        req = await self.__session.request(method, full_url, json=data)

        if not req.content_type == 'application/json':
            return req

        res = await req.json()

        if 'error' in res:
            raise RequestError.get_exception(req.status, res)

        return res

    async def query(self, method: str,
                    path: List[str],
                    params: Optional[dict] = None,
                    data: Optional[dict] = None) -> Union[List, Dict, ClientResponse]:
        """
        Performs request to CouchDB

        :param method: Request method
        :param path: Request path
        :param params: Query parameters
        :param data: Data
        :return: Result of the request
        """

        try:
            return await self._query(method, path, params, data)
        except UnauthorizedError:
            pass

        # We are here because an UnauthorizedError occurred
        # Let's try authentication and try again to execute the request
        await self.authenticate()
        return await self._query(method, path, params, data)

    async def authenticate(self):
        """\
        Starts new session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
        """

        data = {
            'name': self.__username,
            'password': self.__password,
        }
        return await self._query('POST', ['_session'], data=data)

    async def get_session(self):
        """\
        Get current session

        https://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
        """
        return await self._query('GET', ['_session'])

    async def delete_session(self):
        """\
        Close session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#delete--_session
        """
        return await self._query('DELETE', ['_session'])

    @property
    def dbs(self) -> DatabaseProxy:
        return DatabaseProxy(self)

    def get_db(self, name: str) -> Database:
        return Database(self, name)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.__server}')"

    async def shutdown_cleanup(self):
        if self.__session is None:
            return

        s = self.__session
        self.__session = None
        await s.close()

    def __del__(self):
        if self.__session:
            self.__logger.warning("Default session is not closed! "
                                  "You must call Connector.shutdown_cleanup() before exit!")

    @staticmethod
    def _format_query_param(v):
        if isinstance(v, (dict, list)):
            return json.dumps(v)
        if isinstance(v, bool):
            return "true" if v else "false"

        return str(v)
