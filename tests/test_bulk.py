# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from secrets import token_hex

import pytest

from wheelchair.database.database import Database


@pytest.mark.asyncio
async def test_bulk(new_database: Database):
    doc0 = dict(
        _id=token_hex(),
        test_data=token_hex()
    )
    doc1 = dict(
        _id=token_hex(),
        test_data=token_hex()
    )
    doc2 = dict(
        _id=token_hex(),
        test_data=token_hex()
    )

    all_docs = [doc0, doc1, doc2]

    res = await new_database.bulk.docs(all_docs)

    assert res[0]['ok'] == True
    assert res[0]['id'] == doc0['_id']
    assert res[1]['ok'] == True
    assert res[1]['id'] == doc1['_id']
    assert res[2]['ok'] == True
    assert res[2]['id'] == doc2['_id']

    all_get = [
        dict(id=doc0['_id']),
        dict(id=doc1['_id']),
        dict(id=doc2['_id']),
    ]

    res = await new_database.bulk.get(all_get)

    print(res)

    assert res[0]['id'] == doc0['_id']
    assert res[0]['docs'][0]['ok']['test_data'] == doc0['test_data']
    assert res[1]['id'] == doc1['_id']
    assert res[1]['docs'][0]['ok']['test_data'] == doc1['test_data']
    assert res[2]['id'] == doc2['_id']
    assert res[2]['docs'][0]['ok']['test_data'] == doc2['test_data']
