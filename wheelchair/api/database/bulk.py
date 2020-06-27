# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class Bulk:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self, docs: List[dict], revs: Optional[bool] = None) -> List[dict]:
        """\
        Performs bulk get query.

        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_get
        """

        params = dict(revs=revs)
        data = dict(docs=docs)
        res = await self.__connection.query('POST', [self.__database.name, '_bulk_get'], params=params, data=data)
        return res['results']

    async def docs(self, docs: List[dict], new_edits: Optional[bool] = None) -> List[dict]:
        """
        Performs bulk insert/update/delete query.

        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_bulk_docs
        """

        params = dict(new_edits=new_edits)
        data = dict(docs=docs)
        return await self.__connection.query('POST', [self.__database.name, '_bulk_docs'], params=params, data=data)
