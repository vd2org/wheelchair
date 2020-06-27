# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import json
from typing import Any, Optional, Union, List, NamedTuple
from typing import TYPE_CHECKING

from ..utils import StaleOptions

if TYPE_CHECKING:
    from .database import Database
    from .design import Design, PartitionDesign
    from ..connection import Connection
    from .partition import Partition


class ViewQuery(NamedTuple):
    conflicts: Optional[bool] = None
    descending: Optional[bool] = None
    end_key: Optional[Any] = None
    end_key_doc_id: Optional[str] = None
    group: Optional[bool] = None
    group_level: Optional[int] = None
    include_docs: Optional[bool] = None
    attachments: Optional[bool] = None
    att_encoding_info: Optional[bool] = None
    inclusive_end: Optional[bool] = None
    key: Optional[Any] = None
    keys: Optional[Any] = None
    limit: Optional[int] = None
    reduce: Optional[bool] = None
    skip: Optional[int] = None
    sorted: Optional[bool] = None
    stable: Optional[bool] = None
    stale: Optional[Union[bool, StaleOptions]] = None
    start_key: Optional[Any] = None
    start_key_doc_id: Optional[str] = None
    update: Optional[str] = None
    update_seq: Optional[bool] = None


class BaseView:
    def __init__(self, connection: 'Connection', name: str):
        self.__connection = connection
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    async def __call__(self, *,
                       conflicts: Optional[bool] = None,
                       descending: Optional[bool] = None,
                       end_key: Optional[Any] = None,
                       end_key_doc_id: Optional[str] = None,
                       group: Optional[bool] = None,
                       group_level: Optional[int] = None,
                       include_docs: Optional[bool] = None,
                       attachments: Optional[bool] = None,
                       att_encoding_info: Optional[bool] = None,
                       inclusive_end: Optional[bool] = None,
                       key: Optional[Any] = None,
                       keys: Optional[List[Any]] = None,
                       limit: Optional[int] = None,
                       reduce: Optional[bool] = None,
                       skip: Optional[int] = None,
                       sorted: Optional[bool] = None,
                       stable: Optional[bool] = None,
                       stale: Optional[Union[bool, StaleOptions]] = None,
                       start_key: Optional[Any] = None,
                       start_key_doc_id: Optional[str] = None,
                       update: Optional[str] = None,
                       update_seq: Optional[bool] = None,
                       _use_get: bool = False) -> dict:
        """\
        Executes a view function.

        https://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view
        https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view
        """

        params = dict(
            conflicts=conflicts,
            descending=descending,
            end_key=json.dumps(end_key) if _use_get and end_key else end_key,
            end_key_doc_id=end_key_doc_id,
            group=group,
            group_level=group_level,
            include_docs=include_docs,
            attachments=attachments,
            att_encoding_info=att_encoding_info,
            inclusive_end=inclusive_end,
            key=json.dumps(key) if _use_get and key else key,
            keys=keys,
            limit=limit,
            reduce=reduce,
            skip=skip,
            sorted=sorted,
            stable=stable,
            stale=StaleOptions.format(stale),
            start_key=json.dumps(start_key) if _use_get and start_key else start_key,
            start_key_doc_id=start_key_doc_id,
            update=update,
            update_seq=update_seq,
        )

        if _use_get:
            return await self.__connection.query('GET', self._get_path(), params=params)

        return await self.__connection.query('POST', self._get_path(), data=params)

    async def queries(self, *queries: ViewQuery) -> List[dict]:
        """\
        Executes a view function.

        https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view-queries
        """

        queries = [dict(q._asdict()) for q in queries]

        for q in queries:
            q.stale = StaleOptions.format(q.stale)

        data = dict(queries=queries)
        path = self._get_path() + ['queries']

        return await self.__connection.query('POST', path, data=data)

    def _get_path(self) -> List[str]:
        raise NotImplementedError


class ViewProxy:
    def __init__(self, design: 'Design'):
        self.__design = design

    def __call__(self, name: str) -> 'View':
        return View(self.__design, name)

    def __getattr__(self, attr: str) -> 'View':
        return View(self.__design, attr)


class View(BaseView):
    def __init__(self, design: 'Design', name: str):
        self.__database = design.database
        self.__design = design
        self.__name = name

        super().__init__(design.database.connection, name)

    @property
    def design(self) -> Optional['Design']:
        return self.__design

    def _get_path(self) -> List[str]:
        return [self.__database.name, '_design', self.__design.name, '_view', self.__name]


class PartitionViewProxy:
    def __init__(self, design: 'PartitionDesign'):
        self.__design = design

    def __call__(self, name: str) -> 'PartitionView':
        return PartitionView(self.__design, name)

    def __getattr__(self, attr: str) -> 'PartitionView':
        return PartitionView(self.__design, attr)


class PartitionView(BaseView):
    def __init__(self, design: 'PartitionDesign', name: str):
        self.__design = design
        self.__name = name

        super().__init__(design.partition.database.connection, name)

    @property
    def design(self) -> 'PartitionDesign':
        return self.__design

    def _get_path(self) -> List[str]:
        return [
            self.__design.partition.database.name,
            '_partition',
            self.__design.partition.name,
            '_design',
            self.__design.name,
            '_view',
            self.__name
        ]


class AllDocsView(BaseView):
    def __init__(self, database: 'Database'):
        self.__database = database
        self.__name = '_all_docs'

        super().__init__(database.connection, self.__name)

    @property
    def database(self) -> 'Database':
        return self.__database

    def _get_path(self) -> List[str]:
        return [self.__database.name, self.__name]


class PartitionAllDocsView(BaseView):
    def __init__(self, partition: 'Partition'):
        self.__partition = partition
        self.__name = '_all_docs'

        super().__init__(partition.database.connection, self.__name)

    @property
    def partition(self) -> 'Partition':
        return self.__partition

    def _get_path(self) -> List[str]:
        return [self.__partition.database.name, '_partition', self.__partition.name, self.__name]


class LocalDocsView(BaseView):
    def __init__(self, database: 'Database'):
        self.__database = database
        self.__name = '_local_docs'

        super().__init__(database.connection, self.__name)

    @property
    def database(self) -> 'Database':
        return self.__database

    def _get_path(self) -> List[str]:
        return [self.__database.name, self.__name]
