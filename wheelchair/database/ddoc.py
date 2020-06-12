# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

from .doc import Document
from .search import SearchProxy
from .update import UpdateProxy
from .view import ViewProxy

if typing.TYPE_CHECKING:
    from .database import Database


class DesignDocumentsProxy:
    def __init__(self, database: 'Database'):
        self.__database = database

    def __call__(self, name: str) -> 'DesignDocument':
        return DesignDocument(self.__database, name)

    def __getattr__(self, attr: str) -> 'DesignDocument':
        return DesignDocument(self.__database, attr)

    @property
    def doc(self) -> Document:
        return Document(self.__database, doc_type='_design')


class DesignDocument:
    def __init__(self, database: 'Database', name: str):
        self.__connection = database.connection
        self.__database = database
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def database(self) -> 'Database':
        return self.__database

    async def info(self) -> dict:
        """
        Returns information about design document.

        https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc-_info
        """

        path = [self.__database.name, '_design', self.__name, '_info']
        return await self.__connection.query('GET', path)

    @property
    def view(self) -> ViewProxy:
        return ViewProxy(self)

    @property
    def search(self) -> SearchProxy:
        return SearchProxy(self)

    @property
    def update(self) -> UpdateProxy:
        return UpdateProxy(self)
