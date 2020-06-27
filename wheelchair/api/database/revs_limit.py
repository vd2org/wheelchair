# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class RevsLimit:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self) -> int:
        """\
        Returns current revision limit setting.

        https://docs.couchdb.org/en/stable/api/database/misc.html?highlight=purged_infos_limit#get--db-_revs_limit
        """

        return await self.__connection.query('GET', [self.__database.name, '_revs_limit'])

    async def put(self, limit: int) -> bool:
        """\
        Sets the maximum number of document revisions that will be stored in the database.

        https://docs.couchdb.org/en/stable/api/database/misc.html?highlight=purged_infos_limit#put--db-_revs_limit
        """

        res = await self.__connection.query('PUT', [self.__database.name, '_revs_limit'], data=limit)
        return res['ok']
