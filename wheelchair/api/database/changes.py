# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from enum import Enum
from typing import Optional, List, Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class ChangesType(str, Enum):
    main_only = "main_only"
    all_docs = "all_docs"


class Changes:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self, *,
                       doc_ids: Optional[List[str]] = None,
                       doc_filter: Optional[str] = None,
                       view: Optional[str] = None,
                       selector: Optional[dict] = None,
                       conflicts: Optional[bool] = None,
                       descending: Optional[bool] = None,
                       include_docs: Optional[bool] = None,
                       attachments: Optional[bool] = None,
                       att_encoding_info: Optional[bool] = None,
                       last_event_id: Optional[int] = None,
                       limit: Optional[int] = None,
                       since: Union[str, int] = None,
                       style: Optional[ChangesType] = None,
                       seq_interval: Optional[int] = None,
                       timeout: Optional[int] = None) -> dict:
        """\
        Returns a sorted list of changes made to documents in the database.

        If the timeout is set, a longpoll request will be executed.

        https://docs.couchdb.org/en/stable/api/database/changes.html?highlight=feed#get--db-_changes
        https://docs.couchdb.org/en/stable/api/database/changes.html?highlight=feed#post--db-_changes
        """

        data = {
            'doc_ids': doc_ids,
            'selector': selector
        }

        params = {
            'conflicts': conflicts,
            'descending': descending,
            'include_docs': include_docs,
            'attachments': attachments,
            'att_encoding_info': att_encoding_info,
            'last-event-id': last_event_id,
            'limit': limit,
            'since': since,
            'style': style,
            'view': view,
            'seq_interval': seq_interval
        }

        vars = doc_ids is not None, doc_filter is not None, view is not None, selector is not None
        vars = [v for v in vars if v]
        if len(vars) > 1:
            raise TypeError('Only one of doc_ids, doc_filter, view or selector is allowed to be set.')

        if doc_ids is not None:
            params['filter'] = '_doc_ids'
        if view is not None:
            params['filter'] = '_view'
        if selector is not None:
            params['filter'] = '_selector'
        if doc_filter is not None:
            params['filter'] = doc_filter

        if timeout:
            params['feed'] = 'longpoll'
            params['timeout'] = timeout

        return await self.__connection.query('POST', [self.__database.name, '_changes'], params=params, data=data,
                                             timeout=timeout)
