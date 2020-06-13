# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .design import Design


class SearchProxy:
    def __init__(self, ddoc: 'Design'):
        self.__ddoc = ddoc

    def __call__(self, name: str) -> 'Search':
        return Search(self.__ddoc, name)

    def __getattr__(self, attr: str) -> 'Search':
        return Search(self.__ddoc, attr)


class Search:
    def __init__(self, ddoc: 'Design', name: str):
        self.__connection = ddoc.database.connection
        self.__database = ddoc.database
        self.__ddoc = ddoc
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def ddoc(self) -> 'Design':
        return self.__ddoc

    async def __call__(self, *,
                       bookmark: Optional[str] = None,
                       counts: Optional[List[str]] = None,
                       drilldown: Optional[dict] = None,
                       group_field: Optional[str] = None,
                       group_sort: Optional[List[str]] = None,
                       highlight_fields: Optional[List[str]] = None,
                       highlight_pre_tag: Optional[str] = None,
                       highlight_post_tag: Optional[str] = None,
                       highlight_number: Optional[int] = None,
                       highlight_size: Optional[int] = None,
                       include_docs: Optional[bool] = None,
                       include_fields: Optional[List[str]] = None,
                       limit: Optional[int] = None,
                       q: Optional[str] = None,
                       query: Optional[str] = None,
                       ranges: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       stale: Optional[bool] = None) -> dict:
        """\
        Executes a search function.

        https://docs.couchdb.org/en/stable/api/ddoc/search.html#get--db-_design-ddoc-_search-index
        """

        params = dict(
            bookmark=bookmark,
            counts=counts,
            drilldown=drilldown,
            group_field=group_field,
            group_sort=group_sort,
            highlight_fields=highlight_fields,
            highlight_pre_tag=highlight_pre_tag,
            highlight_post_tag=highlight_post_tag,
            highlight_number=highlight_number,
            highlight_size=highlight_size,
            include_docs=include_docs,
            include_fields=include_fields,
            limit=limit,
            q=q,
            query=query,
            ranges=ranges,
            sort=sort,
            stale='ok' if stale else None
        )

        path = [self.__database.name, '_design', self.__ddoc.name, '_search', self.__name]
        return await self.__connection.query('GET', path, params=params)

    async def info(self) -> dict:
        """\
        Get a search index info.

        https://docs.couchdb.org/en/stable/api/ddoc/search.html#get--db-_design-ddoc-_search_info-index
        """

        path = [self.__database.name, '_design', self.__ddoc.name, '_search_info', self.__name]
        return await self.__connection.query('GET', path)
