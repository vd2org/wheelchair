# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from .connection import Connection


@dataclass(frozen=True)
class SessionGetResult:
    ok: bool
    userCtx: dict
    info: dict


@dataclass(frozen=True)
class SessionAuthResult:
    ok: bool
    name: str
    roles: List[str]


class Session:
    def __init__(self, connection: 'Connection', username: str, password: str):
        self.__connection = connection
        self.__username = username
        self.__password = password

    async def __call__(self) -> SessionGetResult:
        """\
        Get current session

        https://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
        """

        res = await self.__connection.direct_query('GET', ['_session'])
        return SessionGetResult(**res)

    async def authenticate(self) -> SessionAuthResult:
        """\
        Starts new session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
        """

        data = {'name': self.__username, 'password': self.__password}

        res = await self.__connection.direct_query('POST', ['_session'], data=data)
        return SessionAuthResult(**res)

    async def delete(self) -> bool:
        """\
        Close session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#delete--_session
        """

        res = await self.__connection.direct_query('DELETE', ['_session'])
        return res['ok']
