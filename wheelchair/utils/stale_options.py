# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from enum import Enum
from typing import Optional, Union


class StaleOptions(str, Enum):
    ok = "ok"
    update_after = "update_after"
    false = "false"

    @staticmethod
    def format(stale: Optional[Union[bool, 'StaleOptions']]) -> 'StaleOptions':
        if stale is True:
            return StaleOptions.ok
        if stale is False:
            return StaleOptions.false

        return stale
