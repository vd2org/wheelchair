# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).

import pytest

from wheelchair import Connection


@pytest.mark.asyncio
async def test_server(admin_connection: Connection):
    res = await admin_connection.server()

    assert res['couchdb'] == 'Welcome'
