# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

from .attachments import Attachments
from .ddoc import DesignDocumentsProxy

if TYPE_CHECKING:
    from ..connection import Connection


class Database:
    def __init__(self, connection: 'Connection', name: str):
        self.__connection = connection
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    async def db_get(self):
        """\
        Get information about database
        """

        return await self.__connection.query('GET', [self.__name])

    async def db_create(self):
        """\
        Creates new database
        """

        return await self.__connection.query('PUT', [self.__name])

    async def db_delete(self):
        """
        Removes database
        """

        return await self.__connection.query('DELETE', [self.__name])

    async def get(self, _id: str):
        return await self.__connection.query('GET', [self.__name, _id])

    async def delete(self, _id: str, _rev: str):
        return await self.__connection.query('DELETE', [self.__name, _id], {'rev': _rev})

    async def insert(self, doc: dict):
        return await self.__connection.query('POST', [self.__name], data=doc)

    async def bulk_insert(self, doc: dict):
        return await self.__connection.query('POST', [self.__name, '_bulk_docs'], data=doc)

    @property
    def ddoc(self) -> DesignDocumentsProxy:
        return DesignDocumentsProxy(self.__connection, self)

    @property
    def attachments(self) -> Attachments:
        return Attachments(self.__connection, self)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__connection)}, '{self.__name}')"
