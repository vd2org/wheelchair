# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class Shards:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self) -> dict:
        """\
        Returns list of the database shars.

        https://docs.couchdb.org/en/stable/api/database/shard.html#get--db-_shards
        """

        path = [self.__database.name, '_shards']
        res = await self.__connection.query('GET', path)
        return res['shards']

    async def doc(self, _id: str) -> dict:
        """\
        Returns information about specific document's shard.

        https://docs.couchdb.org/en/stable/api/database/shard.html#get--db-_shards-docid
        """

        path = [self.__database.name, '_shards', _id]
        return await self.__connection.query('GET', path)

    async def sync(self) -> bool:
        """\
        Forses start shards synchronization for given database.

        https://docs.couchdb.org/en/stable/api/database/shard.html#post--db-_sync_shards
        """

        path = [self.__database.name, '_sync_shards']
        res = await self.__connection.query('POST', path)
        return res['ok']
