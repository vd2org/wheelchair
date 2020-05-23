# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from .utils import SimpleScope


class Server(SimpleScope):
    async def __call__(self):
        """\
        Return instance metadata

        http://docs.couchdb.org/en/latest/api/server/common.html#get--
        """

        return await self._connection.direct_query('GET', [])
