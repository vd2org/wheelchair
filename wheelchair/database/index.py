# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from enum import Enum
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class IndexType(str, Enum):
    json = "json"
    text = "text"


class Index:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self) -> dict:
        """\
        Returns the mango indexes from specified database.

        https://docs.couchdb.org/en/stable/api/database/find.html#get--db-_index
        """

        return await self.__connection.query('GET', [self.__database.name, '_index'])

    async def post(self, index: dict, *,
                   ddoc: Optional[str] = None,
                   name: Optional[str] = None,
                   index_type: Optional[IndexType] = None,
                   selector: Optional[dict] = None,
                   partitioned: Optional[bool]) -> dict:
        """\
        Create a new mango index.

        https://docs.couchdb.org/en/stable/api/database/find.html#post--db-_index
        """

        data = dict(
            index=index,
            ddoc=ddoc,
            name=name,
            type=index_type,
            partial_filter_selector=selector,
            partitioned=partitioned
        )

        return await self.__connection.query('POST', [self.__database.name, '_index'], data=data)
