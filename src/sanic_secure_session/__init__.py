from itsdangerous import Signer, BadData
from sanic import Sanic

from sanic_secure_session.backends import FakeStorageBackend
from sanic_secure_session.session import Session


class SanicSession:
    cookie_name = 'session'

    def __init__(self, app=None, secret_key=None, storage_backend=None):
        self.secret_key = secret_key
        self.storage_backend = storage_backend
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
        signed_sid = request.cookies.get(self.cookie_name)
        try:
            sid = Signer(self.secret_key).unsign(signed_sid).decode('ascii')
        except BadData:
            sid = None

        request['session'] = await self.storage_backend.load(sid) or Session()

    async def save_session(self, request, response):
        # after each request save the session,
        # pass the response to set client cookies
        # await session_interface.save(request, response)
        await self.storage_backend.save(request['session'].sid, request['session'])
        response.cookies[self.cookie_name] = Signer(self.secret_key).sign(request['session'].sid.encode('ascii')).decode('ascii')
