# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from .utils import Query
from .utils import SimpleScope


class Session(SimpleScope):
    async def __call__(self) -> dict:
        """\
        Get current session

        https://docs.couchdb.org/en/latest/api/server/authn.html#get--_session
        """

        query = Query('GET', ['_session'])
        return await self._connection.direct_query(query)

    async def post(self, username: str, password: str) -> dict:
        """\
        Starts new session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#post--_session
        """

        data = {'name': username, 'password': password}

        query = Query('POST', ['_session'], data=data)
        return await self._connection.direct_query(query)

    async def delete(self) -> bool:
        """\
        Close session on server

        https://docs.couchdb.org/en/latest/api/server/authn.html#delete--_session
        """

        query = Query('DELETE', ['_session'])
        res = await self._connection.direct_query(query)
        return res['ok']
