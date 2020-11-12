from asyncio.events import AbstractEventLoop
from typing import Generator, List, Union

from .base import BaseResource
from .insight import InsightSol, InsightValidityCheck

__all__ = [
    'InsightResource',
]


class InsightResource(BaseResource):
    __slots__ = [
        '_sol_keys',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict,
                 loop: AbstractEventLoop = None) -> None:
        super(InsightResource, self).__init__(data, loop=loop)
        self._sol_keys = data.get("sol_keys")
        self._data = data

    def __iter__(self):
        return self

    def __next__(self):
        for sol in self.sols:
            yield sol

    def _process_sols(self) -> Union[Generator[InsightSol, None, None], InsightSol, None]:
        if not (sols := self._sol_keys):
            return None
        elif len(sols) != 1:
            return (InsightSol(sol) for sol in sols)
        else:
            return InsightSol(sols[0])

    @property
    def sols(self) -> Union[Generator[InsightSol, None, None], InsightSol, None]:
        if (sl := f"{self}sols") not in self._cache:
            self._cache[sl] = self._process_sols()
        return self._cache[sl]

    @property
    def validity_checks(self) -> InsightValidityCheck:
        if (vc := f"{self}validity") not in self._cache:
            self._cache[vc] = InsightValidityCheck(self._data.get("validity_checks"))
        return self._cache[vc]

    @property
    def sol_keys(self) -> List[int]:
        return [int(sol) for sol in self._sol_keys]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict,
                  loop: AbstractEventLoop = None) -> "InsightResource":
        return cls(data, loop=loop)
