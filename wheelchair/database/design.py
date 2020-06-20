# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

from .search import SearchProxy
from .update import UpdateProxy
from .view import ViewProxy, PartitionViewProxy

if typing.TYPE_CHECKING:
    from .partition import Partition
    from .database import Database


class DesignProxy:
    def __init__(self, database: 'Database'):
        self.__database = database

    def __call__(self, name: str) -> 'Design':
        return Design(self.__database, name)

    def __getattr__(self, attr: str) -> 'Design':
        return Design(self.__database, attr)


class Design:
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

    async def __call__(self) -> dict:
        """\
        Returns information about design document.

        https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc-_info
        """

        path = [self.__database.name, '_design', self.__name, '_info']
        return await self.__connection.query('GET', path)

    async def compact(self) -> bool:
        """\
        Compacts view indexes of the specific design document.

        https://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact-ddoc
        """

        path = [self.__database.name, '_compact', self.__name]
        res = await self.__connection.query('POST', path)
        return res['ok']

    @property
    def view(self) -> ViewProxy:
        return ViewProxy(self)

    @property
    def search(self) -> SearchProxy:
        return SearchProxy(self)

    @property
    def update(self) -> UpdateProxy:
        return UpdateProxy(self)


class PartitionDesignProxy:
    def __init__(self, database: 'Database'):
        self.__database = database

    def __call__(self, name: str) -> 'PartitionDesign':
        return PartitionDesign(self.__database, name)

    def __getattr__(self, attr: str) -> 'PartitionDesign':
        return PartitionDesign(self.__database, attr)


class PartitionDesign:
    def __init__(self, partition: 'Partition', name: str):
        self.__partition = partition
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def partition(self) -> 'Partition':
        return self.__partition

    @property
    def view(self) -> PartitionViewProxy:
        return PartitionViewProxy(self)
