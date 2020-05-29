# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection import Connection


class Node:
    def __init__(self, connection: 'Connection', name: str):
        self._connection = connection
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def __call__(self) -> str:
        """\
        Returns node's name

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_node-node-name

        """

        res = await self._connection.query('GET', ['_node', self._name])

        return res['name']

    async def stats(self) -> dict:
        """\
        Returns node's statistics

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_node-node-name-_stats

        """

        res = await self._connection.query('GET', ['_node', self._name, '_stats'])

        return res['name']

    async def system(self) -> dict:
        """\
        Returns node's system level statistics

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_node-node-name-_system

        """

        res = await self._connection.query('GET', ['_node', self._name, '_system'])

        return res['name']

    async def restart(self) -> dict:
        """\
        Restarts selected node

        https://docs.couchdb.org/en/latest/api/server/common.html#post--_node-node-name-_restart

        """

        res = await self._connection.query('GET', ['_node', self._name, '_restart'])

        return res['name']
