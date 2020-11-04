import asyncio
import datetime
from collections import namedtuple

import aiohttp
import yarl

from .exceptions import HTTPException, InvalidQuery, RateLimitException
from .resource import APODResource
from .utils import ROUTES, VALID_KEYS

_RLS = namedtuple("Ratelimit Status", ['limit', 'remaining'])


class HTTPClient():
    def __init__(self,
                 session: aiohttp.ClientSession = None,
                 api_key: str = "DEMO KEY",
                 cache_size: int = None,
                 loop: asyncio.AbstractEventLoop = None) -> None:
        self._key = api_key,
        self._cache_size = cache_size,
        try:
            self._loop = loop or asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop()
        self._session = session or aiohttp.ClientSession(
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'apodasync Python Library by @marwynnsomridhivej',
            },
            loop=self._loop,
        )
        self._mapping = {
            'apod': '_get_apod',
        }
        self._bucket = {}
        self._rls = {}

    def replace_key(self, new_key: str) -> None:
        self._key = new_key

    def get_ratelimit(self, route: str) -> namedtuple:
        return self._rls.get(route, None)

    def _ensure_valid_query(self, route: str, **options):
        unsupported = [(key, value) for key, value in options.items()
                       if key not in VALID_KEYS[route]]
        if unsupported:
            raise InvalidQuery(unsupported)

    def _get_url(self, route: str, **options) -> str:
        self._ensure_valid_query(route, **options)
        url = yarl.URL.build(
            scheme="https",
            host="api.nasa.gov",
            path=ROUTES[route],
            query=options,
        )
        return str(url)

    async def request(self, route: str, method: str = None, **options) -> APODResource:
        url = self._generate_url(route, **options)
        for tries in range(5):
            if (rls := self._rls.get(route, None)):
                if rls.remaining == 0:
                    raise RateLimitException()
            await asyncio.sleep(2 ** tries if tries else 0)
            try:
                response, ret = await self._mapping.get(route)(self, url=url, method=method)
                return ret
            except OSError as e:
                if tries < 4 and e.errno in (54, 10054):
                    continue
                raise e
        else:
            raise HTTPException(response.status)

    async def _get_apod(self, url: str = None, **kwargs) -> APODResource:
        async with self._session.get(url) as response:
            raw = await response.read()
            ret = await response.json()
        ret['raw'], ret['query_url'] = raw, url

        limit = int(response.headers.get("X-RateLimit-Limit"))
        remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['apod'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['apod'] = int(datetime.datetime.now())

        return response, APODResource(response=ret, loop=self._loop)
