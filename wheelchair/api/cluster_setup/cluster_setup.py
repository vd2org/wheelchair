# Copyright (C) 2019-2021 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional, List

from ..utils import SimpleScope


class ClusterSetup(SimpleScope):
    async def __call__(self, ensure_dbs_exist: Optional[List[str]] = None) -> dict:
        """\
        Returns the status of the node or cluster, per the cluster setup wizard.

        https://docs.couchdb.org/en/stable/api/server/common.html#get--_cluster_setup
        """

        return await self._connection.query('GET', ['_cluster_setup'], params=dict(ensure_dbs_exist=ensure_dbs_exist))

    async def post(self, action: str, bind_address: Optional[str] = None,
                   username: Optional[str] = None, password: Optional[str] = None,
                   port: Optional[int] = None, node_count: Optional[int] = None,
                   remote_node: Optional[str] = None, remote_current_user: Optional[str] = None,
                   remote_current_password: Optional[str] = None, host: Optional[str] = None,
                   ensure_dbs_exist: Optional[List[str]] = None) -> dict:
        """\
        Configure a node as a single (standalone) node, as part of a cluster, or finalise a cluster.

        https://docs.couchdb.org/en/stable/api/server/common.html#post--_cluster_setup
        """

        data = dict(
            action=action,
            bind_address=bind_address,
            username=username, password=password,
            port=port,
            node_count=node_count,
            remote_node=remote_node,
            remote_current_user=remote_current_user,
            remote_current_password=remote_current_password,
            host=host,
            ensure_dbs_exist=ensure_dbs_exist
        )

        return await self._connection.query('POST', ['_cluster_setup'], data=data)
