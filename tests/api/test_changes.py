# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from asyncio import get_event_loop
from secrets import token_hex

import pytest

from wheelchair.api import Database


@pytest.mark.asyncio
async def test_changes(new_database: Database):
    res = await new_database.changes()

    last_seq = res['last_seq']

    _id = token_hex()

    res = await new_database.doc.put(_id, {})

    _id = res['id']
    _rev = res['rev']

    res = await new_database.changes(since=last_seq)
    changes = res['results']

    assert len(changes) == 1

    upd = changes[0]

    assert upd['id'] == _id
    assert list(upd['changes'][0].items())[0][1] == _rev


@pytest.mark.asyncio
async def test_changes_polling(new_database: Database):
    loop = get_event_loop()
    task = loop.create_task(new_database.changes(since=0, timeout=60_000))

    _id = token_hex()

    res = await new_database.doc.put(_id, {})

    _id = res['id']
    _rev = res['rev']

    res = await task

    changes = res['results']

    assert len(changes) == 1

    upd = changes[0]

    assert upd['id'] == _id
    assert list(upd['changes'][0].items())[0][1] == _rev
