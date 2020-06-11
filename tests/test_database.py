# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from secrets import token_hex

import pytest

from wheelchair.database.database import Database


@pytest.mark.asyncio
async def test_insert(new_database: Database):
    doc = dict(
        _id=token_hex(),
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.insert(doc)

    assert res['id'] == doc['_id']

    res = await new_database.doc(doc['_id'])

    assert res['_id'] == doc['_id']
    assert res['test_data1'] == doc['test_data1']
    assert res['test_data2'] == doc['test_data2']
