import asyncio
import datetime
from collections import namedtuple
from typing import List, Tuple

import aiohttp
import yarl
from aiohttp.client_reqrep import ClientResponse

from .exceptions import HTTPException, RateLimitException
from .resources import (APODResource, CMEAnalysisResource, CMEResource,
                        GSTResource, NEOResource)
from .utils import ROUTES, VALID_KEYS

_RLS = namedtuple("RatelimitStatus", ['limit', 'remaining'])


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
            'neo': '_get_neo',
            'cme': '_get_cme',
            'cme-a': '_get_cme_a',
            'gst': '_get_gst',
            'ips': '_get_ips',
            'flr': '_get_flr',
            'sep': '_get_sep',
            'mpc': '_get_mpc',
            'rbe': '_get_rbe',
            'hss': '_get_hss',
            'wsa-enlil': '_get_wsa_enlil',
        }
        self._bucket = {}
        self._rls = {}

    def replace_key(self, new_key: str) -> None:
        self._key = new_key

    def get_ratelimit(self, route: str) -> namedtuple:
        return self._rls.get(route, None)

    def _ensure_valid_query(self, route: str, **options) -> dict:
        return {
            key: value for key, value in options.items()
            if key in VALID_KEYS[route]
        }

    def _get_url(self, route: str, **options) -> str:
        valid_options = self._ensure_valid_query(route, **options)
        valid_options['api_key'] = self._key
        url = yarl.URL.build(
            scheme="https",
            host="api.nasa.gov",
            path=ROUTES[route],
            query=valid_options,
        )
        return str(url)

    async def request(self, route: str, method: str = None, **options) -> APODResource:
        url = options.get("url") or self._get_url(route, **options)
        for tries in range(5):
            if (rls := self._rls.get(route, None)):
                if rls.remaining == 0:
                    raise RateLimitException()
            await asyncio.sleep(2 ** tries if tries else 0)
            try:
                response, ret = await self._mapping.get(route)(self, url=url, method=method, **options)
                return ret
            except OSError as e:
                if tries < 4 and e.errno in (54, 10054):
                    continue
                raise e
        else:
            raise HTTPException(response.status)

    async def _get_apod(self, url: str = None, **kwargs) -> Tuple[ClientResponse, APODResource]:
        async with self._session.get(url) as response:
            raw = await response.read()
            ret = await response.json()
            ret['raw'], ret['query_url'], ret['code'] = raw, url, response.status
            limit = int(response.headers.get("X-RateLimit-Limit"))
            remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['apod'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['apod'] = int(datetime.datetime.now())
        return response, APODResource(ret, loop=self._loop)

    async def _get_neo(self, url: str = None, **kwargs) -> Tuple[ClientResponse, NEOResource]:
        search_type = kwargs.get("search_type")
        async with self._session.get(url) as response:
            ret = await response.json()
            ret['query_url'], ret['code'], ret['search_type'] = url, response.status, search_type
            limit = int(response.headers.get("X-RateLimit-Limit"))
            remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['neo'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['neo'] = int(datetime.datetime.now())
        return response, NEOResource(ret, loop=self._loop)

    async def _get_cme(self, url: str = None, **kwargs) -> Tuple[ClientResponse, List[CMEResource]]:
        async with self._session.get(url) as response:
            ret = await response.json()
            for subdict in ret:
                subdict['query_url'], subdict['code'] = url, response.status
            limit = int(response.headers.get("X-RateLimit-Limit"))
            remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['cme'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['cme'] = int(datetime.datetime.now())
        return response, [CMEResource(data, loop=self._loop) for data in ret]

    async def _get_cme_a(self, url: str = None, **kwargs) -> Tuple[ClientResponse, List[CMEAnalysisResource]]:
        async with self._session.get(url) as response:
            ret = await response.json()
            for subdict in ret:
                subdict['query_url'], subdict['code'] = url, response.status
            limit = int(response.headers.get("X-RateLimit-Limit"))
            remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['cme'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['cme'] = int(datetime.datetime.now())
        return response, [CMEAnalysisResource(data, loop=self._loop) for data in ret]

    async def _get_gst(self, url: str = None, **kwargs) -> Tuple[ClientResponse, List[GSTResource]]:
        async with self._session.get(url) as response:
            ret = await response.json()
            for subdict in ret:
                subdict['query_url'], subdict['code'] = url, response.status
            limit = int(response.headers.get("X-RateLimit-Limit"))
            remaining = int(response.headers.get("X-RateLimit-Remaining"))
        self._rls['gst'] = _RLS(limit, remaining)
        if limit - remaining == 1:
            self._bucket['gst'] = int(datetime.datetime.now())
        return response, [GSTResource(data, loop=self._loop) for data in ret]
