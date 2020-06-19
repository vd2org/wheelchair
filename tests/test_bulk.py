# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


import pytest

from wheelchair.database.database import Database


@pytest.mark.asyncio
async def test_bulk(new_database: Database):
    docs = [
        dict(value=1),
        dict(value=2),
        dict(value=3),
        dict(value=4),
        dict(value=5),
    ]

    res = await new_database.bulk.docs(docs)

    assert len(res) == 5

    for row in res:
        assert row['ok']
        assert isinstance(row['id'], str)
        assert isinstance(row['rev'], str)

    docs = [dict(id=e['id']) for e in res]
    res = await new_database.bulk(docs)

    assert len(res) == 5

    for row in res:
        assert isinstance(row['id'], str)
        assert len(row['docs']) == 1

        docs = row['docs'][0]

        assert 'ok' in docs

        doc = docs['ok']

        assert doc['value'] in {1, 2, 3, 4, 5}
