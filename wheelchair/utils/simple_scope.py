# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import typing

if typing.TYPE_CHECKING:
    from ..connection import Connection


class SimpleScope:
    def __init__(self, connection: 'Connection'):
        self._connection = connection
