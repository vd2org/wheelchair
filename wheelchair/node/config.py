# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection import Connection


class Config:
    def __init__(self, connection: 'Connection', name: str):
        self._connection = connection
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def connection(self) -> 'Connection':
        return self._connection

    async def __call__(self, section: Optional[str] = None, key: Optional[str] = None) -> Any:
        """\
        Returns the entire node's config or a selected section of the config or a single key of the config

        https://docs.couchdb.org/en/latest/api/server/configuration.html#get--_node-node-name-_config
        https://docs.couchdb.org/en/latest/api/server/configuration.html#get--_node-node-name-_config-section
        """

        return await self._connection.query('GET', ['_node', self._name, '_config', section, key])

    async def put(self, section: str, key: str, value: Any) -> Any:
        """\
        Updates a configuration value

        https://docs.couchdb.org/en/latest/api/server/configuration.html#put--_node-node-name-_config-section-key
        """

        return await self._connection.query('PUT', ['_node', self._name, '_config', section, key], data=value)

    async def delete(self, section: str, key: str) -> Any:
        """\
        Deletes a configuration value

        https://docs.couchdb.org/en/latest/api/server/configuration.html#delete--_node-node-name-_config-section-key
        """

        return await self._connection.query('DELETE', ['_node', self._name, '_config', section, key])

    async def reload(self) -> bool:
        """\
        Reloads the configuration from disk

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_node-node-name-_system
        """

        res = await self._connection.query('POST', ['_node', self._name, '_config', '_reload'])
        return res['ok']
