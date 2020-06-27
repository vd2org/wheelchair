# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, List, Union, Tuple
from typing import TYPE_CHECKING

from .design import PartitionDesignProxy
from .view import PartitionAllDocsView
from ..utils import StaleOptions

if TYPE_CHECKING:
    from .database import Database


class PartitionProxy:
    def __init__(self, database: 'Database'):
        self.__database = database
        self.__connection = database.connection

    def __call__(self, name: str) -> 'Partition':
        return Partition(self.__database, name)

    def __getattr__(self, attr) -> 'Partition':
        return Partition(self.__database, attr)


class Partition:
    def __init__(self, database: 'Database', name: str):
        self.__database = database
        self.__connection = database.connection
        self.__name = name

    @property
    def database(self) -> 'Database':
        return self.__database

    @property
    def name(self) -> str:
        return self.__name

    async def __call__(self) -> dict:
        """\
        Get information about the database partition.

        https://docs.couchdb.org/en/stable/api/partitioned-dbs.html#get--db-_partition-partition
        """

        return await self.__connection.query('GET', [self.database.name, '_partition', self.__name])

    @property
    def all_docs(self) -> PartitionAllDocsView:
        """\
        Returns View scope for all_docs of the given database's partition.

        https://docs.couchdb.org/en/stable/api/partitioned-dbs.html#get--db-_partition-partition-_all_docs
        """

        return PartitionAllDocsView(self)

    @property
    def design(self) -> PartitionDesignProxy:
        return PartitionDesignProxy(self)

    async def find(self, selector: dict, *,
                   limit: Optional[int] = None,
                   skip: Optional[int] = None,
                   sort: Optional[dict] = None,
                   fields: Optional[List[str]] = None,
                   use_index: Optional[Union[str, Tuple[str]]] = None,
                   r: Optional[int] = None,
                   bookmark: Optional[str] = None,
                   update: Optional[bool] = None,
                   stable: Optional[bool] = None,
                   stale: Optional[Union[bool, StaleOptions]] = None,
                   execution_stats: Optional[bool] = None) -> dict:
        """\
        Executes find request using Mango declarative syntax for the given partition.

        https://docs.couchdb.org/en/stable/api/partitioned-dbs.html#get--db-_partition-partition_id-_find
        """

        data = dict(
            selector=selector,
            limit=limit,
            skip=skip,
            sort=sort,
            fields=fields,
            use_index=use_index,
            r=r,
            bookmark=bookmark,
            update=update,
            stable=stable,
            stale=StaleOptions.format(stale),
            execution_stats=execution_stats,
        )

        path = [self.database.name, '_partition', self.__name, '_find']
        return await self.__connection.query('POST', path, data=data)

    async def explain(self,
                      selector: dict,
                      limit: Optional[int] = None,
                      skip: Optional[int] = None,
                      sort: Optional[dict] = None,
                      fields: Optional[List[str]] = None,
                      use_index: Optional[Union[str, Tuple[str]]] = None,
                      r: Optional[int] = None,
                      bookmark: Optional[str] = None,
                      update: Optional[bool] = None,
                      stable: Optional[bool] = None,
                      stale: Optional[Union[bool, StaleOptions]] = None,
                      execution_stats: Optional[bool] = None) -> dict:
        """\
        Explain with index will be used in find request for the given partition.

        https://docs.couchdb.org/en/stable/api/partitioned-dbs.html#get--db-_partition-partition_id-_explain
        """

        data = dict(
            selector=selector,
            limit=limit,
            skip=skip,
            sort=sort,
            fields=fields,
            use_index=use_index,
            r=r,
            bookmark=bookmark,
            update=update,
            stable=stable,
            stale=StaleOptions.format(stale),
            execution_stats=execution_stats,
        )

        path = [self.database.name, '_partition', self.__name, '_explain']
        return await self.__connection.query('POST', path, data=data)
