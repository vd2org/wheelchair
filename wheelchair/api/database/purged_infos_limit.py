# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class PurgedInfosLimit:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self) -> int:
        """\
        Gets the current purged documents limit setting.

        https://docs.couchdb.org/en/stable/api/database/misc.html?highlight=purged_infos_limit#get--db-_purged_infos_limit
        """

        return await self.__connection.query('GET', [self.__database.name, '_purged_infos_limit'])

    async def put(self, limit: int) -> bool:
        """\
        Sets the maximum number of purges (requested purged Ids with their revisions) that will be tracked in the
        database, even after compaction has occurred.

        https://docs.couchdb.org/en/stable/api/database/misc.html?highlight=purged_infos_limit#put--db-_purged_infos_limit
        """

        res = await self.__connection.query('PUT', [self.__database.name, '_purged_infos_limit'], data=limit)
        return res['ok']
