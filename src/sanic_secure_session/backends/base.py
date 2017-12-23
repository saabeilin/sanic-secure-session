from abc import ABC, abstractmethod


class StorageBackend(ABC):
    @abstractmethod
    async def load(self, sid):
        pass

    @abstractmethod
    async def save(self, sid, data, expire=None):
        pass
