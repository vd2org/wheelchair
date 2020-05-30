# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair import Connection


@pytest.mark.asyncio
async def test_session(admin_connection: Connection):
    await admin_connection.session.authenticate()
    res = await admin_connection.session()

    assert res.userCtx['name'] == 'admin'
    assert len(res.userCtx['roles']) > 0


@pytest.mark.asyncio
async def test_authenticate(admin_connection: Connection):
    res = await admin_connection.session.authenticate()

    assert res.name == 'admin'
    assert isinstance(res.roles, list)


@pytest.mark.asyncio
async def test_delete(admin_connection: Connection):
    await admin_connection.session.authenticate()
    await admin_connection.session.delete()
    res = await admin_connection.session()

    assert res.userCtx['name'] is None
    assert res.userCtx['roles'] == []
