# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from io import BytesIO
from secrets import token_hex

import pytest

from wheelchair.api import Database
from wheelchair.api.utils.query import StreamResponse


@pytest.mark.asyncio
async def test_attachment(new_database: Database):
    _id = token_hex()

    data = b"Test " * 10000

    res = await new_database.doc.put(_id, {})

    assert res['id'] == _id

    res = await new_database.att.put(_id, 'my_data', 'application/octet-stream', data, rev=res['rev'])

    doc_rev = res['rev']

    res = await new_database.att(_id, 'my_data')

    assert isinstance(res, StreamResponse)

    assert res.content_type == 'application/octet-stream'

    res_data = await res.stream.read()

    assert data == res_data

    await new_database.att.delete(_id, 'my_data', doc_rev)


@pytest.mark.asyncio
async def test_attachment_stream(new_database: Database):
    _id = token_hex()

    data = b"Test " * 10000

    res = await new_database.doc.put(_id, {})

    async def loader(data: bytes):
        stream = BytesIO(data)
        stream.seek(0)

        while True:
            chunk = stream.read(1024)
            if not len(chunk):
                break

            yield chunk

    assert res['id'] == _id

    await new_database.att.put(_id, 'my_data', 'application/octet-stream', loader(data), rev=res['rev'])

    res = await new_database.att(_id, 'my_data')

    assert isinstance(res, StreamResponse)

    res_data = await res.stream.read()

    assert data == res_data
