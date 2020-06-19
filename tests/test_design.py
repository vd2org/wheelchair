# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair.database.database import Database


@pytest.mark.asyncio
async def test_design(new_database: Database):
    map_func = "function (doc) {if (doc.type === 'doc') {emit(doc._id, doc.value);}}"
    ddoc = {"views": {"my_docs": {"map": map_func}}}

    await new_database.ddoc.put('my_docs', ddoc)

    await new_database.post(dict(type='doc', value=1))
    await new_database.post(dict(type='doc', value=2))
    await new_database.post(dict(type='doc', value=3))
    await new_database.post(dict(type='another_doc', value='a'))
    await new_database.post(dict(type='another_doc', value='b'))

    design = new_database.design('my_docs')
    res = await design()

    assert res['name'] == 'my_docs'


@pytest.mark.asyncio
async def test_compact(new_database: Database):
    map_func = "function (doc) {if (doc.type === 'doc') {emit(doc._id, doc.value);}}"
    ddoc = {"views": {"my_docs": {"map": map_func}}}

    await new_database.ddoc.put('my_docs', ddoc)

    design = new_database.design('my_docs')
    res = await design.compact()

    assert res


@pytest.mark.asyncio
async def test_view(new_database: Database):
    map_func = "function (doc) {if (doc.type === 'doc') {emit(doc._id, doc.value);}}"
    ddoc = {"views": {"my_docs": {"map": map_func}}}

    await new_database.ddoc.put('my_docs', ddoc)

    await new_database.post(dict(type='doc', value=1))
    await new_database.post(dict(type='doc', value=2))
    await new_database.post(dict(type='doc', value=3))
    await new_database.post(dict(type='another_doc', value='a'))
    await new_database.post(dict(type='another_doc', value='b'))

    view = new_database.design('my_docs').view('my_docs')
    res = await view()

    rows = res['rows']

    assert len(rows) == 3

    values = {v['value'] for v in rows}

    assert 1 in values
    assert 2 in values
    assert 3 in values


@pytest.mark.asyncio
async def test_design_search(new_database: Database):
    pass  # TODO: implement me!


@pytest.mark.asyncio
async def test_design_update(new_database: Database):
    pass  # TODO: implement me!
