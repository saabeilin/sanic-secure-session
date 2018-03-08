from sanic_secure_session import Session
from sanic_secure_session.backends.base import StorageBackend

try:
    import ujson as json
except ImportError:
    import json


class RedisStorageBackend(StorageBackend):
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    async def load(self, sid):
        raw_data = await (await self.redis_connection()).get(sid)
        if not raw_data:
            return None
        try:
            data = json.loads(raw_data)
        except:
            return None
        return Session(sid, **data) if data else None

    async def save(self, sid, data, expire=None):
        raw_data = json.dumps(data)
        await (await self.redis_connection()).set(sid, raw_data, expire)

    async def remove(self, sid):
        await (await self.redis_connection()).delete(sid)
