from sanic import Sanic

from sanic_secure_session.backends import FakeStorageBackend
from sanic_secure_session.session import Session


class SanicSession:
    cookie_name = 'session'

    def __init__(self, app=None, storage_backend=None):
        self.storage_backend = None or FakeStorageBackend()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Sanic):
        """hook on request start etc."""
        app.register_middleware(self.open_session, 'request')
        app.register_middleware(self.save_session, 'response')

    async def open_session(self, request):
        # before each request initialize a session
        # using the client's request
        # await session_interface.open(request)
        sid = request.cookies.get(self.cookie_name)
        request['session'] = await self.storage_backend.load(sid) or Session()

    async def save_session(self, request, response):
        # after each request save the session,
        # pass the response to set client cookies
        # await session_interface.save(request, response)
        await self.storage_backend.save(request['session'].sid, request['session'])
        response.cookies[self.cookie_name] = request['session'].sid
