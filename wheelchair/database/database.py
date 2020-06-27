# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, Dict, List, Union, Tuple
from typing import TYPE_CHECKING

from .attachment import Attachment, DesignAttachment, LocalAttachment
from .bulk import Bulk
from .changes import Changes
from .design import DesignProxy
from .doc import Document, LocalDocument, DesignDocument
from .index import Index
from .purged_infos_limit import PurgedInfosLimit
from .revs_limit import RevsLimit
from .security import Security
from .shards import Shards
from .view import AllDocsView, LocalDocsView
from ..utils import StaleOptions

if TYPE_CHECKING:
    from ..connection import Connection


class DatabaseProxy:
    def __init__(self, connection: 'Connection'):
        self.__connection = connection

    def __call__(self, name: str) -> 'Database':
        return Database(self.__connection, name)

    def __getattr__(self, attr) -> 'Database':
        return Database(self.__connection, attr)


class Database:
    def __init__(self, connection: 'Connection', name: str):
        self.__connection = connection
        self.__name = name

    @property
    def connection(self) -> 'Connection':
        return self.__connection

    @property
    def name(self) -> str:
        return self.__name

    async def __call__(self) -> dict:
        """\
        Get information about database.

        https://docs.couchdb.org/en/stable/api/database/common.html#get--db
        """

        return await self.__connection.query('GET', [self.__name])

    async def create(self):
        """\
        Creates new database.

        https://docs.couchdb.org/en/stable/api/database/common.html#put--db
        """

        return await self.__connection.query('PUT', [self.__name])

    async def delete(self):
        """
        Removes database.

        https://docs.couchdb.org/en/stable/api/database/common.html#delete--db
        """

        return await self.__connection.query('DELETE', [self.__name])

    async def post(self, doc: dict, batch: Optional[bool] = None) -> dict:
        """\
        Inserts new document into database.

        https://docs.couchdb.org/en/stable/api/database/common.html#post--db
        """

        params = dict(batch="ok" if batch else None)
        return await self.__connection.query('POST', [self.__name], params=params, data=doc)

    @property
    def all_docs(self) -> AllDocsView:
        """\
        Returns View scope for all_docs of the database.

        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs
        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs-queries
        """

        return AllDocsView(self)

    @property
    def doc(self) -> Document:
        return Document(self)

    @property
    def att(self) -> Attachment:
        return Attachment(self)

    @property
    def ddoc(self) -> DesignDocument:
        """\
        Returns Document scope for design documents.

        https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc
        https://docs.couchdb.org/en/stable/api/ddoc/common.html#put--db-_design-ddoc
        https://docs.couchdb.org/en/stable/api/ddoc/common.html#copy--db-_design-ddoc
        """

        return DesignDocument(self)

    @property
    def ddoc_att(self) -> DesignAttachment:
        """\
        Returns Attachment scope for design documents.

        https://docs.couchdb.org/en/stable/api/ddoc/common.html#head--db-_design-ddoc-attname
        https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc-attname
        https://docs.couchdb.org/en/stable/api/ddoc/common.html#put--db-_design-ddoc-attname
        https://docs.couchdb.org/en/stable/api/ddoc/common.html#delete--db-_design-ddoc-attname
        """

        return DesignAttachment(self)

    @property
    def design(self) -> DesignProxy:
        return DesignProxy(self)

    @property
    def bulk(self) -> Bulk:
        return Bulk(self)

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
        Executes find request using Mango declarative syntax.

        https://docs.couchdb.org/en/stable/api/database/find.html#post--db-_find
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

        return await self.__connection.query('POST', [self.__name, '_find'], data=data)

    @property
    def index(self) -> Index:
        return Index(self)

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
        Explain with index will be used in find request.

        https://docs.couchdb.org/en/stable/api/database/find.html#post--db-_explain
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

        return await self.__connection.query('POST', [self.__name, '_explain'], data=data)

    @property
    def shards(self) -> Shards:
        return Shards(self)

    @property
    def changes(self) -> Changes:
        return Changes(self)

    async def compact(self) -> bool:
        """\
        Compacts the entire database.

        https://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact
        """

        res = await self.__connection.query('POST', [self.name, '_compact'])
        return res['ok']

    async def view_cleanup(self) -> bool:
        """\
        Removes unused view indexes.

        https://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_view_cleanup
        """

        res = await self.__connection.query('POST', [self.__name, '_view_cleanup'])
        return res['ok']

    @property
    def security(self) -> Security:
        return Security(self)

    async def purge(self, docs: Dict[str, List[str]]) -> dict:
        """\
        Removes old document's revisions.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_purge
        """

        return await self.__connection.query('POST', [self.__name, '_purge'], data=docs)

    @property
    def purged_infos_limit(self) -> PurgedInfosLimit:
        return PurgedInfosLimit(self)

    async def missing_revs(self, docs: Dict[str, List[str]]) -> dict:
        """\
        With given a list of document revisions, returns the document revisions that do not exist in the database.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_missing_revs
        """

        res = await self.__connection.query('POST', [self.__name, '_missing_revs'], data=docs)
        return res['missing_revs']

    @property
    def revs_limit(self) -> RevsLimit:
        return RevsLimit(self)

    async def revs_diff(self, docs: Dict[str, List[str]]) -> dict:
        """\
        Given a set of document/revision IDs, returns the subset
        of those that do not correspond to revisions stored in the database.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_revs_diff
        """

        return await self.__connection.query('POST', [self.__name, '_revs_diff'], data=docs)

    @property
    def local_docs(self) -> LocalDocsView:
        """\
        Returns View scope for local_docs of the database.

        https://docs.couchdb.org/en/stable/api/local.html#get--db-_local_docs
        https://docs.couchdb.org/en/stable/api/local.html#post--db-_local_docs
        """

        return LocalDocsView(self)

    @property
    def local(self) -> LocalDocument:
        """\
        Returns Document scope for local documents.

        https://docs.couchdb.org/en/stable/api/local.html#get--db-_local-docid
        https://docs.couchdb.org/en/stable/api/local.html#put--db-_local-docid
        https://docs.couchdb.org/en/stable/api/local.html#delete--db-_local-docid
        https://docs.couchdb.org/en/stable/api/local.html#copy--db-_local-docid
        """

        return LocalDocument(self)

    @property
    def local_att(self) -> LocalAttachment:
        """\
        Returns Attachment scope for local documents.

        WARNING: This is probably an undocumented feature.
        """

        return LocalAttachment(self)
