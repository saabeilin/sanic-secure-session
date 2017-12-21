from ..session import Session

_storage = {}


class FakeStorageBackend:

    async def load(self, sid):
        data = _storage.get(sid, None)
        return Session(sid, **data) if data else None

    async def save(self, sid, data):
        _storage[sid] = data
