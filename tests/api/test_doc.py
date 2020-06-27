# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from secrets import token_hex

import pytest

from wheelchair.api import Database, NotFoundError


@pytest.mark.asyncio
async def test_create(new_database: Database):
    _id = token_hex()
    doc = dict(
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.doc.put(_id, doc)

    assert res['id'] == _id

    res = await new_database.doc(_id)

    assert res['_id'] == _id
    assert res['test_data1'] == doc['test_data1']
    assert res['test_data2'] == doc['test_data2']


@pytest.mark.asyncio
async def test_delete(new_database: Database):
    _id = token_hex()
    doc = dict(
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.doc.put(_id, doc)

    assert res['id'] == _id

    res = await new_database.doc.delete(_id, res['rev'])

    assert res['id'] == _id

    try:
        await new_database.doc(_id)
    except NotFoundError:
        pass
    else:
        assert False, 'Document still exist!'


@pytest.mark.asyncio
async def test_copy(new_database: Database):
    _id = token_hex()
    doc = dict(
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.doc.put(_id, doc)

    assert res['id'] == _id

    dst_id = token_hex()

    await new_database.doc.copy(_id, dst_id)

    res = await new_database.doc(dst_id)

    assert res['_id'] == dst_id
    assert res['test_data1'] == doc['test_data1']
    assert res['test_data2'] == doc['test_data2']


@pytest.mark.asyncio
async def test_copy_to_exist(new_database: Database):
    _id = token_hex()
    dst_id = token_hex()
    doc = dict(
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.doc.put(_id, doc)

    assert res['id'] == _id

    res = await new_database.doc.put(dst_id, doc)

    assert res['id'] == dst_id

    await new_database.doc.copy(_id, dst_id, dst_rev=res['rev'])

    res = await new_database.doc(dst_id)

    assert res['_id'] == dst_id
    assert res['test_data1'] == doc['test_data1']
    assert res['test_data2'] == doc['test_data2']
