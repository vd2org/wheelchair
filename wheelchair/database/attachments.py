# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

if typing.TYPE_CHECKING:
    from ..connection import Connection
    from .database import Database


class Attachments:
    def __init__(self, connection: 'Connection', database: 'Database'):
        self.__connection = connection
        self.__database = database

    async def get(self, _id: str, attachment: str):
        return await self.__connection.query('GET', [self.__database.name, _id, attachment])
