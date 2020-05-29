import pytest

from wheelchair import Connection

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
async def admin_connection() -> Connection:
    connection = Connection.from_string("http://admin:admin@localhost/")

    yield connection

    await connection.shutdown_cleanup()
