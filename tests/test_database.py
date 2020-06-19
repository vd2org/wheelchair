# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from secrets import token_hex

import pytest

from wheelchair.database.database import Database


@pytest.mark.asyncio
async def test_database(new_database: Database):
    res = await new_database()

    assert res['db_name'] == new_database.name


@pytest.mark.asyncio
async def test_post(new_database: Database):
    doc = dict(
        _id=token_hex(),
        test_data1=token_hex(),
        test_data2=token_hex()
    )

    res = await new_database.post(doc)

    assert res['id'] == doc['_id']

    res = await new_database.doc(doc['_id'])

    assert res['_id'] == doc['_id']
    assert res['test_data1'] == doc['test_data1']
    assert res['test_data2'] == doc['test_data2']


@pytest.mark.asyncio
async def test_all_docs(new_database: Database):
    await new_database.post(dict(value=1))
    await new_database.post(dict(value=2))
    await new_database.post(dict(value=3))

    res = await new_database.all_docs(include_docs=True)

    rows = res['rows']

    assert len(rows) == 3

    values = {v['doc']['value'] for v in rows}

    assert 1 in values
    assert 2 in values
    assert 3 in values


@pytest.mark.asyncio
async def test_ddoc(new_database: Database):
    map_func = "function (doc) {emit(doc._id, null);}"
    ddoc = {"views": {"my_docs": {"map": map_func}}}

    await new_database.ddoc.put('my_docs', ddoc)

    res = await new_database.ddoc('my_docs')

    assert res['_id'] == '_design/my_docs'
    assert res['views'] == ddoc['views']


@pytest.mark.asyncio
async def test_ddoc_att(new_database: Database):
    pass  # TODO: implement me!


@pytest.mark.asyncio
async def test_find(new_database: Database):
    await new_database.post(dict(type='doc', value=1))
    await new_database.post(dict(type='doc', value=2))
    await new_database.post(dict(type='doc', value=3))
    await new_database.post(dict(type='other_doc', value=4))
    await new_database.post(dict(type='other_doc', value=5))

    selector = {'type': 'doc'}
    res = await new_database.find(selector)

    assert isinstance(res['warning'], str)

    docs = res['docs']

    assert len(docs) == 3

    values = {doc['value'] for doc in docs}

    assert 1 in values
    assert 2 in values
    assert 3 in values


@pytest.mark.asyncio
async def test_index(new_database: Database):
    idx = {'fields': ['value']}
    idx_selector = {'type': {'$eq': 'doc'}}
    res = await new_database.index.post(idx, name='my_idx', ddoc='my_idx', selector=idx_selector)

    assert res['result'] == 'created'
    assert res['name'] == 'my_idx'

    res = await new_database.index()

    assert len(res['indexes']) == 2

    names = {e['name'] for e in res['indexes']}

    assert {'_all_docs', 'my_idx'} == names

    await new_database.post(dict(type='doc', value=1))
    await new_database.post(dict(type='doc', value=2))
    await new_database.post(dict(type='doc', value=3))
    await new_database.post(dict(type='other_doc', value=4))
    await new_database.post(dict(type='other_doc', value=5))

    selector = {'value': {'$gt': 0}}
    res = await new_database.find(selector, use_index='my_idx')

    assert 'warning' not in res

    docs = res['docs']

    assert len(docs) == 3

    values = {doc['value'] for doc in docs}

    assert 1 in values
    assert 2 in values
    assert 3 in values

    res = await new_database.index.delete('my_idx', 'my_idx')

    assert res


@pytest.mark.asyncio
async def test_explain(new_database: Database):
    idx = {'fields': ['value']}
    idx_selector = {'type': {'$eq': 'doc'}}
    res = await new_database.index.post(idx, name='my_idx', ddoc='my_idx', selector=idx_selector)

    assert res['result'] == 'created'
    assert res['name'] == 'my_idx'

    selector = {'value': {'$gt': 0}}
    res = await new_database.explain(selector, use_index='my_idx')

    assert res['index']['ddoc'] == '_design/my_idx'
    assert res['index']['name'] == 'my_idx'
    assert res['index']['type'] == 'json'

    selector = {'value': {'$gt': 0}}
    res = await new_database.explain(selector, use_index='unknown_index')

    assert res['index']['ddoc'] == None
    assert res['index']['name'] == '_all_docs'
    assert res['index']['type'] == 'special'


@pytest.mark.asyncio
async def test_shards(new_database: Database):
    res = await new_database.shards()
    assert len(res.keys()) > 0

    res = await new_database.post(dict(type='doc', value=1))
    res = await new_database.shards.doc(res['id'])
    assert len(res.keys()) > 0

    res = await new_database.shards.sync()
    assert res


@pytest.mark.asyncio
async def test_compact(new_database: Database):
    res = await new_database.compact()

    assert res


@pytest.mark.asyncio
async def test_view_cleanup(new_database: Database):
    res = await new_database.view_cleanup()

    assert res
