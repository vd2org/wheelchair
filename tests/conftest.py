# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair import Connection

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
async def admin_connection() -> Connection:
    connection = Connection.from_string("http://admin:admin@localhost/")

    yield connection

    await connection.shutdown_cleanup()
