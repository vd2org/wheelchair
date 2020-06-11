# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

from .auth import Auth
from ..utils import Query

if TYPE_CHECKING:
    from ..connection import Connection


class CookieAuth(Auth):
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    async def __call__(self, connection: 'Connection', params: Query) -> Query:
        return params

    async def authenticate(self, connection: 'Connection'):
        await connection.session.post(self._username, self._password)
