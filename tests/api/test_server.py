# Copyright (C) 2019-2021 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair import Connection


@pytest.mark.asyncio
async def test_server(admin_connection: Connection):
    res = await admin_connection.server()

    assert res['couchdb'] == 'Welcome'


@pytest.mark.asyncio
async def test_active_tasks(admin_connection: Connection):
    res = await admin_connection.server.active_tasks()

    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_all_dbs(admin_connection: Connection):
    res = await admin_connection.server.all_dbs()

    assert isinstance(res, list)
    assert isinstance(res[0], str)


@pytest.mark.asyncio
async def test_dbs_info(admin_connection: Connection):
    res = await admin_connection.server.dbs_info(['_users'])

    assert isinstance(res, list)
    assert res[0]['key'] == '_users'


@pytest.mark.asyncio
async def test_membership(admin_connection: Connection):
    res = await admin_connection.server.membership()

    assert isinstance(res['all_nodes'], list)
    assert isinstance(res['cluster_nodes'], list)


@pytest.mark.asyncio
async def test_up(admin_connection: Connection):
    res = await admin_connection.server.up()

    assert res['status'] == "ok"


@pytest.mark.asyncio
async def test_uuids(admin_connection: Connection):
    res = await admin_connection.server.uuids()

    assert isinstance(res, list)
    assert len(res) == 1

    res = await admin_connection.server.uuids(5)

    assert isinstance(res, list)
    assert len(res) == 5
