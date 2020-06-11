# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import List, Optional, NamedTuple


class Query(NamedTuple):
    method: str
    path: List[str]
    params: Optional[dict] = None
    data: Optional[dict] = None
    headers: Optional[dict] = None
