from datetime import datetime

from itsdangerous import Signer
from sanic import Sanic

from sanic_secure_session.session import Session


class SanicSession:
    cookie_name = 'session'

    def __init__(self, app=None, secret_key=None, storage_backend=None,
                 domain=None,
                 ttl=None,
                 secure=False,
                 http_only=True,
                 same_site=None,
                 ):
        self.secret_key = secret_key
        self.storage_backend = storage_backend
        self.domain = domain
        self.ttl = ttl
        self.secure = secure
        self.http_only = http_only
        self.same_site = same_site
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Sanic):
        """hook on request start etc."""
        app.register_middleware(self.open_session, 'request')
        app.register_middleware(self.save_session, 'response')

    async def open_session(self, request):
        # before each request initialize a session
        # using the client's request
        signed_sid = request.cookies.get(self.cookie_name)
        try:
            sid = Signer(self.secret_key).unsign(signed_sid).decode('ascii')
        except:
            sid = None
        session = await self.storage_backend.load(sid) if sid else None
        request['session'] = session or Session()

    async def save_session(self, request, response):
        # after each request save the session,
        # pass the response to set client cookies
        await self.storage_backend.save(request['session'].sid, request['session'])
        session_cookie = Signer(self.secret_key).sign(request['session'].sid.encode('ascii')).decode('ascii')
        response.cookies[self.cookie_name] = session_cookie
        if self.ttl:
            response.cookies[self.cookie_name]['max-age'] = self.ttl.total_seconds()
            response.cookies[self.cookie_name]['expires'] = datetime.utcnow() + self.ttl
        if self.domain:
            response.cookies[self.cookie_name]['domain'] = self.domain
        if self.http_only:
            response.cookies[self.cookie_name]['httponly'] = True
