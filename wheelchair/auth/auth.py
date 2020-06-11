# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

from ..utils import Query

if TYPE_CHECKING:
    from ..connection import Connection


class Auth:
    async def __call__(self, connection: 'Connection', query: Query) -> Query:
        raise NotImplemented

    async def authenticate(self, connection: 'Connection'):
        raise NotImplemented
