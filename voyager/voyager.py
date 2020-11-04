import asyncio
import datetime
import re
from typing import List, Union
from voyager.utils import BASE_URL

import aiohttp

from .http import HTTPClient
from .resource import APODResource, NEOResource


_DATE_RX = re.compile(r'[1|2][0|9][0-9]{2}')


class Client():
    def __init__(self,
                 session: aiohttp.ClientSession = None,
                 api_key: str = "DEMO_KEY",
                 loop: asyncio.AbstractEventLoop = None) -> None:
        self._key = api_key
        try:
            self._loop = loop or asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop()
        self._http_client = HTTPClient(session=session,
                                       api_key=self._key,
                                       cache_size=self._cache_size,
                                       loop=loop)

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, new_key: str) -> None:
        self._key = new_key
        self._http_client.replace_key(self._key)

    def _validate_dates(self,
                        dates: Union[List[datetime.datetime], List[str]]) -> None:
        if isinstance(dates, str):
            if not re.match(_DATE_RX, dates):
                raise ValueError("Date of type str must be formatted in "
                                 "YYYY-MM-DD form")
        else:
            for date in dates:
                if isinstance(date, str) and not re.match(_DATE_RX, date):
                    raise ValueError("Dates of type str must be formatted in "
                                     "YYYY-MM-DD form")

    async def apod(self, date: Union[datetime.datetime, str] = None, hd: bool = True) -> APODResource:
        """Returns an image from the NASA Astronomy Photo of the Day API

        :param date: the date to search for, defaults to the current date
        :type date: Union[datetime.datetime, str], optional
        :param hd: retrieve the URL for the high resolution image or not, defaults to True
        :type hd: bool, optional
        """
        self._validate_dates(date)
        options = {
            'date': date,
            'hd': hd,
        }
        ret = await self._http_client.request(route='apod', method="GET", **options)
        return ret

    async def neo_feed(self, start_date: Union[datetime.datetime, str, None] = None,
                       end_date: Union[datetime.datetime, str, None] = None) -> NEOResource:
        if not (start_date or end_date):
            ret = await self._http_client.request(route="neo", search_type="feed-none")
        else:
            dates = {}
            if start_date:
                dates['start_date'] = start_date
            if end_date:
                dates['end_date'] = end_date
            ret = await self._http_client.request(
                route="neo",
                search_type="feed-query",
                **dates,
            )
        return ret

    async def neo_lookup(self, asteroid_id) -> NEOResource:
        return await self._http_client.request(
            route="neo",
            search_type="lookup",
            url=f"{BASE_URL}/neo/rest/v1/neo/{asteroid_id}?api_key={self._key}"
        )

    async def neo_browse(self) -> NEOResource:
        return await self._http_client.request(
            route="neo",
            search_type="browse",
            url=f"{BASE_URL}/neo/rest/v1/neo/browse?api_key={self._key}"
        )
