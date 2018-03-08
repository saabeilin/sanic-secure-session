from sanic_secure_session.backends.base import StorageBackend
from ..session import Session

_storage = {}


class FakeStorageBackend(StorageBackend):

    async def load(self, sid):
        data = _storage.get(sid, None)
        return Session(sid, **data) if data else None

    async def save(self, sid, data, expire=None):
        _storage[sid] = data

    async def remove(self, sid):
        del _storage[sid]
