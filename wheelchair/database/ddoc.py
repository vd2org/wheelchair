# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

from .view import ViewProxy

if typing.TYPE_CHECKING:
    from ..connection import Connection
    from .database import Database


class DesignDocumentsProxy:
    def __init__(self, connection: 'Connection', database: 'Database'):
        self.__connection = connection
        self.__database = database

    def __call__(self, name: str) -> 'DesignDocument':
        return DesignDocument(self.__connection, self.__database, name)

    def __getattr__(self, attr: str) -> 'DesignDocument':
        return DesignDocument(self.__connection, self.__database, attr)


class DesignDocument:
    def __init__(self, connection: 'Connection', database: 'Database', name: str):
        self.__connection = connection
        self.__database = database
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def view(self) -> ViewProxy:
        return ViewProxy(self.__connection, self.__database, self)
