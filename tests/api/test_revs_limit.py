# Copyright (C) 2019-2021 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair.api import Database


@pytest.mark.asyncio
async def test_revs_limit(new_database: Database):
    res = await new_database.revs_limit()

    assert isinstance(res, int)

    res = await new_database.revs_limit.put(100)

    assert res

    res = await new_database.revs_limit()

    assert res == 100
