# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).
from io import IOBase
from typing import TYPE_CHECKING, Optional, Generator, AsyncGenerator, Union

from ..utils.query import StreamResponse, StreamRequest

if TYPE_CHECKING:
    from .database import Database


class BaseAttachment:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database

    @property
    def database(self) -> 'Database':
        return self.__database

    async def __call__(self, _id: str, name: str, *, rev: Optional[str] = None) -> StreamResponse:
        """\
        Returns the attachment by the specified _id.

        https://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
        https://docs.aiohttp.org/en/stable/streams.html?highlight=StreamReader#aiohttp.StreamReader
        """

        return await self.__connection.query('GET', self._get_path(_id, name), params=dict(rev=rev), as_stream=True)

    async def put(self, _id: str, name: str, content_type: str,
                  stream: Union[Generator, AsyncGenerator, bytes, bytearray, IOBase], *,
                  rev: Optional[str]):
        """\
        Uploads the attachment into the document.

        https://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
        https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-uploads
        """

        stream_req = StreamRequest(content_type, stream)
        return await self.__connection.query('PUT', self._get_path(_id, name), params=dict(rev=rev), data=stream_req)

    async def delete(self, _id: str, name: str, rev: str, batch: Optional[bool] = None) -> dict:
        """\
        Deletes the attachment specified by name from the document _id.

        https://docs.couchdb.org/en/stable/api/document/attachments.html#delete--db-docid-attname
        """

        params = dict(rev=rev, batch=batch)

        return await self.__connection.query('DELETE', self._get_path(_id, name), params=params)

    def _get_path(self, _id: str, name: str):
        raise NotImplementedError


class Attachment(BaseAttachment):
    def _get_path(self, _id: str, name: str):
        return [self.database.name, _id, name]


class DesignAttachment(BaseAttachment):
    def _get_path(self, _id: str, name: str):
        return [self.database.name, '_design', _id, name]


class LocalAttachment(BaseAttachment):
    def _get_path(self, _id: str, name: str):
        return [self.database.name, '_local', _id, name]
