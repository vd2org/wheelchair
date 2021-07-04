# Copyright (C) 2019-2021 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from typing import Optional

from ..utils import SimpleScope


class Scheduler(SimpleScope):
    async def jobs(self, limit: Optional[int] = None, skip: Optional[int] = None) -> dict:
        """\
        List of transient replication jobs.

        https://docs.couchdb.org/en/stable/api/server/common.html#get--_scheduler-jobs
        """

        params = dict(limit=limit, skip=skip)

        return await self._connection.query('GET', ['_scheduler', 'jobs'], params=params)

    async def docs(self, replicator_db: Optional[str] = None, limit: Optional[int] = None,
                   skip: Optional[int] = None) -> dict:
        """\
        List of persistent replication jobs.

        https://docs.couchdb.org/en/stable/api/server/common.html#get--_scheduler-docs
        https://docs.couchdb.org/en/stable/api/server/common.html#get--_scheduler-docs-replicator_db
        """

        params = dict(limit=limit, skip=skip)

        path = ['_scheduler', 'docs']
        if replicator_db:
            path.append(replicator_db)

        return await self._connection.query('GET', path, params=params)

    async def doc(self, replicator_db: str, doc_id: str) -> dict:
        """\
        Get a persistent replication job.

        https://docs.couchdb.org/en/stable/api/server/common.html#get--_scheduler-jobs
        """

        return await self._connection.query('GET', ['_scheduler', 'docs', replicator_db, doc_id])
