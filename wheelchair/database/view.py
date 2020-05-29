# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

if typing.TYPE_CHECKING:
    from ..connection import Connection
    from .database import Database
    from .ddoc import DesignDocument


class ViewProxy:
    def __init__(self, connection: 'Connection', database: 'Database', ddoc: 'DesignDocument'):
        self.__connection = connection
        self.__database = database
        self.__ddoc = ddoc

    def __call__(self, name: str) -> 'View':
        return View(self.__connection, self.__database, self.__ddoc, name)

    def __getattr__(self, attr: str) -> 'View':
        return View(self.__connection, self.__database, self.__ddoc, attr)


class View:
    def __init__(self, connection: 'Connection', database: 'Database', ddoc: 'DesignDocument', name: str):
        self.__connection = connection
        self.__database = database
        self.__ddoc = ddoc
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    async def view(self, **kwargs):
        """
        Executes view function

        More info: https://docs.couchdb.org/en/latest/api/ddoc/views.html

        """

        path = [self.__database.name, '_design', self.__ddoc.name, '_view', self.__name]
        return await self.__connection.query('GET', path, kwargs)
