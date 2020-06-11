# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import List, NamedTuple
from typing import TYPE_CHECKING

from .utils import Query
from .utils import SimpleScope

if TYPE_CHECKING:
    pass


class SessionGetResult(NamedTuple):
    ok: bool
    userCtx: dict
    info: dict


class SessionAuthResult(NamedTuple):
    ok: bool
    name: str
    roles: List[str]


class Session(SimpleScope):
    async def __call__(self) -> SessionGetResult:
        """\
        Get current session

        https://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
        """

        query = Query('GET', ['_session'])
        res = await self._connection.direct_query(query)
        return SessionGetResult(**res)

    async def post(self, username: str, password: str) -> SessionAuthResult:
        """\
        Starts new session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
        """

        data = {'name': username, 'password': password}

        query = Query('POST', ['_session'], data=data)
        res = await self._connection.direct_query(query)
        return SessionAuthResult(**res)

    async def delete(self) -> bool:
        """\
        Close session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#delete--_session
        """

        query = Query('DELETE', ['_session'])
        res = await self._connection.direct_query(query)
        return res['ok']
