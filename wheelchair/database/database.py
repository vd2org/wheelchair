# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional
from typing import TYPE_CHECKING

from .attachments import Attachments
from .bulk import Bulk
from .ddoc import DesignDocumentsProxy
from .doc import Documents

if TYPE_CHECKING:
    from ..connection import Connection


class DatabaseProxy:
    def __init__(self, connection: 'Connection'):
        self.__connection = connection

    def __call__(self, name: str) -> 'Database':
        return Database(self.__connection, name)

    def __getattr__(self, attr) -> 'Database':
        return Database(self.__connection, attr)


class Database:
    def __init__(self, connection: 'Connection', name: str):
        self.__connection = connection
        self.__name = name

    @property
    def connection(self) -> 'Connection':
        return self.__connection

    @property
    def name(self) -> str:
        return self.__name

    async def __call__(self) -> dict:
        """\
        Get information about database.

        https://docs.couchdb.org/en/stable/api/database/common.html#get--db
        """

        return await self.__connection.query('GET', [self.__name])

    async def create(self):
        """\
        Creates new database.

        https://docs.couchdb.org/en/stable/api/database/common.html#put--db
        """

        return await self.__connection.query('PUT', [self.__name])

    async def delete(self):
        """
        Removes database.

        https://docs.couchdb.org/en/stable/api/database/common.html#delete--db
        """

        return await self.__connection.query('DELETE', [self.__name])

    async def insert(self, doc: dict, batch: Optional[bool] = None) -> dict:
        """
        Inserts new document into database.

        https://docs.couchdb.org/en/stable/api/database/common.html#post--db
        """

        params = dict(batch="ok" if batch else None)
        return await self.__connection.query('POST', [self.__name], params=params, data=doc)

    @property
    def doc(self) -> Documents:
        return Documents(self)

    @property
    def bulk(self) -> Bulk:
        return Bulk(self)

    @property
    def ddoc(self) -> DesignDocumentsProxy:
        return DesignDocumentsProxy(self.__connection, self)

    @property
    def attachments(self) -> Attachments:
        return Attachments(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__connection)}, '{self.__name}')"
