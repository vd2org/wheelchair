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
