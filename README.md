Gotta get your sessions fast!
=============================

Cookie-based sessions are still a common way to track users's sessions. 
Flask and Django have really good support for server-side sessions, but not Sanic yet.
So `sanic-secure-session` is an attempt to create a simple yet enough secure session support for Sanic.

 * Server-side sessions (currently only Redis backend implemented)
 * Signed session cookie (sure, using `itsdangerous`)
 * Easily extensible backends (only serialization and storage-related logic there)

## Usage example


```python
from datetime import timedelta

import asyncio_redis
from sanic import Sanic
from sanic.response import text

from sanic_secure_session import SanicSession
from sanic_secure_session.backends.redis import RedisStorageBackend


class RedisPool:
    """
    A simple wrapper class that allows you to share a connection
    pool across your application.
    """
    _pool = None

    async def get_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(
                host='localhost', port=6379, poolsize=10
            )

        return self._pool


redis_pool = RedisPool()

storage_backend = RedisStorageBackend(redis_connection=redis_pool.get_pool)

app = Sanic()
SanicSession(app, secret_key='aeNgaif6Ieyishoh', storage_backend=storage_backend,
             ttl=timedelta(minutes=1), http_only=True, secure=True)


@app.route("/")
async def index(request):
    # interact with the session like a normal dict
    if not request['session'].get('foo'):
        request['session']['foo'] = 0

    request['session']['foo'] += 1

    return text({
        'cookies': request.cookies,
        'session': request['session']
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

```

