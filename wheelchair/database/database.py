# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, Dict, List
from typing import TYPE_CHECKING

from .attachments import Attachments
from .bulk import Bulk
from .ddoc import DesignDocumentsProxy
from .doc import Document
from .security import Security
from .shards import Shards
from .view import View

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
        """
        Inserts new document into database.

        https://docs.couchdb.org/en/stable/api/database/common.html#post--db
        """

        params = dict(batch="ok" if batch else None)
        return await self.__connection.query('POST', [self.__name], params=params, data=doc)

    @property
    def all(self) -> View:
        """\
        Returns View scope for all_docs of the database.

        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs
        https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs-queries
        """
        return View(self, None, '_all_docs')

    @property
    def bulk(self) -> Bulk:
        return Bulk(self)

    @property
    def ddoc(self) -> DesignDocumentsProxy:
        return DesignDocumentsProxy(self)

    @property
    def shards(self) -> Shards:
        return Shards(self)

    async def compact(self) -> bool:
        """
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

    def purge(self, docs: Dict[List[str]]) -> dict:
        """\
        Removes old document's revisions.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_purge
        """

        return await self.__connection.query('POST', [self.__name, '_purge'], data=docs)

    @property
    def purged_infos_limit(self):
        # TODO: implement me!
        raise NotImplementedError

    def missing_revs(self, docs: Dict[List[str]]) -> dict:
        """\
        With given a list of document revisions, returns the document revisions that do not exist in the database.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_missing_revs
        """

        res = await self.__connection.query('POST', [self.__name, '_purge'], data=docs)
        return res['missing_revs']

    @property
    def revs_limit(self):
        # TODO: implement me!
        raise NotImplementedError

    def revs_diff(self, docs: Dict[List[str]]) -> dict:
        """\
        Given a set of document/revision IDs, returns the subset
        of those that do not correspond to revisions stored in the database.

        https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_revs_diff
        """

        return await self.__connection.query('POST', [self.__name, '_revs_diff'], data=docs)

    @property
    def attachments(self) -> Attachments:
        return Attachments(self)

    @property
    def doc(self) -> Document:
        return Document(self)
