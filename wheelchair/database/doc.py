# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class Documents:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    async def __call__(self, _id: str, _rev: Optional[str] = None, *,
                       attachments: Optional[bool] = None,
                       att_encoding_info: Optional[bool] = None,
                       atts_since: Optional[List[str]] = None,
                       conflicts: Optional[bool] = None,
                       deleted_conflicts: Optional[bool] = None,
                       latest: Optional[bool] = None,
                       local_seq: Optional[bool] = None,
                       meta: Optional[bool] = None,
                       open_revs: Optional[List[str]] = None,
                       revs: Optional[bool] = None,
                       revs_info: Optional[bool] = None) -> dict:
        """
        Returns document by the specified _id.

        https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
        """

        params = dict(
            attachments=attachments,
            att_encoding_info=att_encoding_info,
            atts_since=atts_since,
            conflicts=conflicts,
            deleted_conflicts=deleted_conflicts,
            latest=latest,
            local_seq=local_seq,
            meta=meta,
            open_revs=open_revs,
            revs=revs,
            revs_info=revs_info,
        )

        return await self.__connection.query('GET', [self.__database.name, _id], params=params)

    async def put(self, _id: str, doc: dict, *,
                  rev: Optional[str] = None,
                  batch: Optional[bool] = None,
                  new_edits: Optional[bool] = True) -> dict:
        """
        Put new document or update existing document.

        https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid

        """

        params = dict(
            rev=rev,
            batch="ok" if batch else None,
            new_edits=new_edits
        )

        return await self.__connection.query('PUT', [self.__database.name, _id], params=params, data=doc)

    async def delete(self, _id: str, _rev: str, *, batch: Optional[bool] = None) -> dict:
        """
        Deletes existing document.

        https://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
        """

        params = dict(
            rev=_rev,
            batch="ok" if batch else None,
        )

        return await self.__connection.query('DELETE', [self.__database.name, _id], params=params)

    async def copy(self, _id: str, dst_id: str, *,
                   _rev: Optional[str] = None,
                   dst_rev: Optional[str] = None,
                   batch: Optional[bool] = None) -> dict:
        """
        Deletes existing document.

        https://docs.couchdb.org/en/stable/api/document/common.html#copy--db-docid
        """

        headers = dict(
            Destination=f'{dst_id}?rev={dst_rev}' if dst_rev else dst_id
        )

        params = dict(
            rev=_rev,
            batch="ok" if batch else None,
        )

        return await self.__connection.query('COPY', [self.__database.name, _id], params=params, headers=headers)
