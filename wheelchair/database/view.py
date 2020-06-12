# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import json
from enum import Enum
from typing import Any, Optional, Union, List, NamedTuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection import Connection
    from .database import Database
    from .ddoc import DesignDocument


class StaleOptions(str, Enum):
    ok = "ok"
    update_after = "update_after"
    false = "false"


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
                       update_seq: Optional[bool] = None) -> dict:
        """
        Executes a view function.

        https://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view
        """

        if stale is True:
            stale = StaleOptions.ok
        elif stale is False:
            stale = StaleOptions.false

        params = dict(
            conflicts=conflicts,
            descending=descending,
            end_key=json.dumps(end_key),
            end_key_doc_id=end_key_doc_id,
            group=group,
            group_level=group_level,
            include_docs=include_docs,
            attachments=attachments,
            att_encoding_info=att_encoding_info,
            inclusive_end=inclusive_end,
            key=json.dumps(key),
            keys=keys,
            limit=limit,
            reduce=reduce,
            skip=skip,
            sorted=sorted,
            stable=stable,
            stale=stale,
            start_key=json.dumps(start_key),
            start_key_doc_id=start_key_doc_id,
            update=update,
            update_seq=update_seq,
        )

        path = [self.__database.name, '_design', self.__ddoc.name, '_view', self.__name]
        return await self.__connection.query('GET', path, params=params)

    async def queries(self, *queries: ViewQuery) -> List[dict]:
        """
        Executes a view function.

        https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view-queries
        """

        queries = [dict(q._asdict()) for q in queries]

        for q in queries:
            if q.stale == True:
                q.stale = StaleOptions.ok
            elif q.stale == False:
                q.stale = StaleOptions.false

        data = dict(queries=queries)

        path = [self.__database.name, '_design', self.__ddoc.name, '_view', self.__name, 'queries']
        return await self.__connection.query('POST', path, data=data)
