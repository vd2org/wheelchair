# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database


class Attachments:
    def __init__(self, database: 'Database'):
        self.__connection = database.connection
        self.__database = database
