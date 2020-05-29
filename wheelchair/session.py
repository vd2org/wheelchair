# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from dataclasses import dataclass
import typing

if typing.TYPE_CHECKING:
    from .connection import Connection


@dataclass(frozen=True)
class SessionResult:
    ok: bool
    userCtx: dict
    info: dict


class Session:
    def __init__(self, connection: 'Connection', username: str, password: str):
        self.__connection = connection
        self.__username = username
        self.__password = password

    async def __call__(self) -> SessionResult:
        """\
        Get current session

        https://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
        """

        res = await self.__connection.direct_query('GET', ['_session'])
        return SessionResult(**res)

    async def authenticate(self):
        """\
        Starts new session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
        """

        data = {'name': self.__username, 'password': self.__password}
        return await self.__connection.direct_query('POST', ['_session'], data=data)

    async def delete(self):
        """\
        Close session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#delete--_session
        """
        return await self.__connection.direct_query('DELETE', ['_session'])
