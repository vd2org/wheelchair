# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class Security:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self) -> dict:
        """\
        Returns the current security object from the specified database.

        https://docs.couchdb.org/en/stable/api/database/security.html#get--db-_security
        """

        return await self.__connection.query('GET', [self.__database.name, '_security'])

    async def put(self,
                  admins_names: List[str],
                  admins_roles: List[str],
                  members_names: List[str],
                  members_roles: List[str]) -> bool:
        """\
        Sets the security object for the given database.

        https://docs.couchdb.org/en/stable/api/database/security.html#put--db-_security
        """

        data = dict(
            admins=dict(
                names=admins_names,
                roles=admins_roles
            ),
            members=dict(
                names=members_names,
                roles=members_roles
            ),
        )

        res = await self.__connection.query('PUT', [self.__database.name, '_security'], data=data)
        return res['ok']
