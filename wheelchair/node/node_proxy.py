# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional
from typing import TYPE_CHECKING

from .node import Node

if TYPE_CHECKING:
    from ..connection import Connection


class NodeProxy:
    def __init__(self, connection: 'Connection'):
        self.__connection = connection

    def __call__(self, name: Optional[str] = "_local") -> 'Node':
        return Node(self.__connection, name)

    def __getattr__(self, attr) -> 'Node':
        return Node(self.__connection, attr)
