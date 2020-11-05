import asyncio
import datetime
import re
from typing import List, Union

import aiohttp

from .exceptions import VoyagerException
from .http import HTTPClient
from .resources import (APODResource, CMEAnalysisResource, CMEResource,
                        GSTResource, NEOResource)
from .utils import BASE_URL

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
                        dates: Union[List[datetime.datetime], List[str], None]) -> None:
        if not dates:
            return True
        elif isinstance(dates, str):
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
        return await self._http_client.request(route='apod', method="GET", **options)

    async def neo_feed(self, start_date: Union[datetime.datetime, str, None] = None,
                       end_date: Union[datetime.datetime, str, None] = None) -> NEOResource:
        if not (start_date or end_date):
            ret = await self._http_client.request(
                route="neo",
                method="GET",
                search_type="feed-none"
            )
        else:
            dates = {}
            if start_date:
                dates['start_date'] = start_date
            if end_date:
                dates['end_date'] = end_date
            self._validate_dates(dates)
            ret = await self._http_client.request(
                route="neo",
                method="GET",
                search_type="feed-query",
                **dates,
            )
        return ret

    async def neo_lookup(self, asteroid_id) -> NEOResource:
        return await self._http_client.request(
            route="neo",
            method="GET",
            search_type="lookup",
            url=f"{BASE_URL}/neo/rest/v1/neo/{asteroid_id}?api_key={self._key}"
        )

    async def neo_browse(self) -> NEOResource:
        return await self._http_client.request(
            route="neo",
            method="GET",
            search_type="browse",
            url=f"{BASE_URL}/neo/rest/v1/neo/browse?api_key={self._key}"
        )

    async def cme(self,
                  start_date: Union[datetime.datetime, str] = None,
                  end_date: Union[datetime.datetime, str] = None) -> List[CMEResource]:
        if not (start_date or end_date):
            ret = await self._http_client.request(
                route="cme",
                method="GET",
            )
        else:
            dates = {}
            if start_date:
                dates['startDate'] = start_date
            if end_date:
                dates['endDate'] = end_date
            self._validate_dates(dates)
            ret = await self._http_client.request(
                route="cme",
                method="GET",
                **dates,
            )
        return ret

    def _validate_cme_catalog(self, catalog: str) -> None:
        if not catalog.upper() in ["ALL", "SWRC_CATALOG", "JANG_ET_AL_CATALOG"]:
            raise VoyagerException(f"Invalid catalogue specified: {catalog.upper()}")

    async def cme_analysis(self,
                           start_date: Union[datetime.datetime, str] = None,
                           end_date: Union[datetime.datetime, str] = None,
                           most_accurate_only: bool = True,
                           complete_entry_only: bool = True,
                           speed: int = 0,
                           half_angle: int = 0,
                           catalog: str = "ALL",
                           keyword: str = "NONE") -> List[CMEAnalysisResource]:
        self._validate_cme_catalog(catalog)
        if not (start_date or end_date):
            ret = await self._http_client.request(
                route="cme-a",
                method="GET",
                mostAccuraetOnly=most_accurate_only,
                completeEntryOnly=complete_entry_only,
                speed=speed,
                halfAngle=half_angle,
                catalog=catalog,
                keyword=keyword,
            )
        else:
            dates = {}
            if start_date:
                dates['startDate'] = start_date
            if end_date:
                dates['endDate'] = end_date
            self._validate_dates(dates)
            ret = await self._http_client.request(
                route="cme-a",
                method="GET",
                **dates,
                mostAccuraetOnly=most_accurate_only,
                completeEntryOnly=complete_entry_only,
                speed=speed,
                halfAngle=half_angle,
                catalog=catalog,
                keyword=keyword,
            )
        return ret

    async def gst(self,
                  start_date: Union[datetime.datetime, str] = None,
                  end_date: Union[datetime.datetime, str] = None) -> List[GSTResource]:
        if not (start_date or end_date):
            ret = await self._http_client.request(
                route="gst",
                method="GET",
            )
        else:
            dates = {}
            if start_date:
                dates['startDate'] = start_date
            if end_date:
                dates['endDate'] = end_date
            self._validate_dates(dates)
            ret = await self._http_client.request(
                route="gst",
                method="GET",
                **dates,
            )
        return ret
