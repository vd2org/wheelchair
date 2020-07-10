# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, Union, List

from ..utils import SimpleScope


class Server(SimpleScope):
    async def __call__(self) -> dict:
        """\
        Return instance metadata.

        http://docs.couchdb.org/en/latest/api/server/common.html#get--
        """

        return await self._connection.query('GET', [])

    async def active_tasks(self) -> List[dict]:
        """\
        Returns database's active tasks.

        https://docs.couchdb.org/en/latest/api/server/common.html#active-tasks
        """

        return await self._connection.query('GET', ['_active_tasks'])

    async def all_dbs(self,
                      start_key: Optional[Union[list, dict]] = None,
                      end_key: Optional[Union[list, dict]] = None,
                      skip: Optional[int] = None,
                      limit: Optional[int] = None,
                      descending: Optional[bool] = None) -> List[str]:
        """\
        Returns a list of all the databases.

        http://docs.couchdb.org/en/latest/api/server/common.html#get--_all_dbs
        """

        params = dict(
            start_key=start_key,
            end_key=end_key,
            skip=skip,
            limit=limit,
            descending=descending
        )

        return await self._connection.query('GET', ['_all_dbs'], params=params)

    async def dbs_info(self, keys: List[str]) -> List[dict]:
        """\
        Returns info of the selected databases.

        https://docs.couchdb.org/en/latest/api/server/common.html#post--_dbs_info
        """

        return await self._connection.query('POST', ['_dbs_info'], data=dict(keys=keys))

    async def membership(self) -> dict:
        """\
        Returns list of the cluster nodes.

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_membership
        """

        return await self._connection.query('GET', ['_membership'])

    async def up(self) -> dict:
        """\
        Ping the node.

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_up
        """

        return await self._connection.query('GET', ['_up'])

    async def uuids(self, count: int = 1) -> List[str]:
        """\
        Generate UUIDs by the server.

        https://docs.couchdb.org/en/latest/api/server/common.html#get--_uuids
        """

        res = await self._connection.query('GET', ['_uuids'], params=dict(count=count))
        return res['uuids']
