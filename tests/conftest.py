# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from secrets import token_hex

import pytest

from wheelchair import Connection
from wheelchair.api import Database

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
async def admin_connection() -> Connection:
    connection = Connection.from_string("http://admin:admin@localhost/")

    yield connection

    await connection.shutdown_cleanup()


@pytest.fixture
async def new_database(admin_connection: Connection) -> Database:
    db = admin_connection.db('test_' + token_hex())

    await db.create()

    yield db

    await db.delete()
