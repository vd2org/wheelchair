# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).

from io import IOBase
from typing import Union, List, Optional, NamedTuple, AsyncGenerator, Generator

from aiohttp import StreamReader


class StreamRequest(NamedTuple):
    content_type: str
    stream: Union[Generator, AsyncGenerator, bytes, bytearray, IOBase]


class StreamResponse(NamedTuple):
    content_type: str
    stream: StreamReader


class Query(NamedTuple):
    method: str
    path: List[str]
    params: Optional[dict] = None
    data: Optional[Union[dict, StreamRequest]] = None
    headers: Optional[dict] = None
