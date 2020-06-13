# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Any, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .design import Design


class UpdateProxy:
    def __init__(self, ddoc: 'Design'):
        self.__ddoc = ddoc

    def __call__(self, name: str) -> 'Update':
        return Update(self.__ddoc, name)

    def __getattr__(self, attr: str) -> 'Update':
        return Update(self.__ddoc, attr)


class Update:
    def __init__(self, ddoc: 'Design', name: str):
        self.__connection = ddoc.database.connection
        self.__database = ddoc.database
        self.__ddoc = ddoc
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def ddoc(self) -> 'Design':
        return self.__ddoc

    async def __call__(self, _id: Optional[str], data: Any) -> dict:
        """\
        Executes an update function.

        https://docs.couchdb.org/en/stable/api/ddoc/render.html#post--db-_design-ddoc-_update-func
        https://docs.couchdb.org/en/stable/api/ddoc/render.html#put--db-_design-ddoc-_update-func-docid
        """

        if _id:
            path = [self.__database.name, '_design', self.__ddoc.name, '_update', self.__name, _id]
            return await self.__connection.query('PUT', path, data=data)

        path = [self.__database.name, '_design', self.__ddoc.name, '_update', self.__name]
        return await self.__connection.query('POST', path, data=data)
