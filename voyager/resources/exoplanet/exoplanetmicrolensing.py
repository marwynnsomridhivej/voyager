from typing import Union


_ATTRS = {
    "plntname":         Union[str, None],
    "ra_str":           Union[str, None],
    "dec_str":          Union[str, None],
    "mlmassplnj":       Union[float, None],
    "mlmassplnjerr1":   Union[float, None],
    "mlmassplnjerr2":   Union[float, None],
    "mlmassplnjlim":    Union[int, None],
    "mlmassplne":       Union[float, None],
    "mlmassplneerr1":   Union[float, None],
    "mlmassplneerr2":   Union[float, None],
    "mlmassplnelim":    Union[int, None],
    "mlsmaproj":        Union[float, None],
    "mlsmaprojerr1":    Union[float, None],
    "mlsmaprojerr2":    Union[float, None],
    "mlsmaprojlim":     Union[int, None],
    "mlmasslens":       Union[float, None],
    "mlmasslenserr1":   Union[float, None],
    "mlmasslenserr2":   Union[float, None],
    "mlmasslenslim":    Union[int, None],
    "mldistl":          Union[float, None],
    "mldistlerr1":      Union[float, None],
    "mldistlerr2":      Union[float, None],
    "mldistllim":       Union[int, None],
    "mldists":          Union[float, None],
    "mldistserr1":      Union[float, None],
    "mldistserr2":      Union[float, None],
    "mldistslim":       Union[int, None],
    "mltsepmin":        Union[float, None],
    "mltsepminerr1":    Union[float, None],
    "mltsepminerr2":    Union[float, None],
    "mltsepminlim":     Union[int, None],
    "mlsepminnorm":     Union[float, None],
    "mlsepminnormerr1": Union[float, None],
    "mlsepminnormerr2": Union[float, None],
    "mlsepminnormlim":  Union[int, None],
    "mlxtimeein":       Union[float, None],
    "mlxtimeeinerr1":   Union[float, None],
    "mlxtimeeinerr2":   Union[float, None],
    "mlxtimeeinlim":    Union[int, None],
    "mlradsnorm":       Union[float, None],
    "mlradsnormerr1":   Union[float, None],
    "mlradsnormerr2":   Union[float, None],
    "mlradsnormlim":    Union[int, None],
    "mlsepinsnorp":     Union[float, None],
    "mlsepinsnorperr1": Union[float, None],
    "mlsepinsnorperr2": Union[float, None],
    "mlsepinsnorplim":  Union[int, None],
    "mlmassratio":      Union[float, None],
    "mlmassratioerr1":  Union[float, None],
    "mlmassratioerr2":  Union[float, None],
    "mlmassratiolim":   Union[int, None],
    "mlangstlax":       Union[float, None],
    "mlangstlaxerr1":   Union[float, None],
    "mlangstlaxerr2":   Union[float, None],
    "mlangstlaxlim":    Union[int, None],
    "mlmagis":          Union[float, None],
    "mlmagiserr1":      Union[float, None],
    "mlmagiserr2":      Union[float, None],
    "mlmagislim":       Union[int, None],
    "mlmagibl":         Union[float, None],
    "mlmagiblerr1":     Union[float, None],
    "mlmagiblerr2":     Union[float, None],
    "mlmagibllim":      Union[int, None],
    "mlradeinang":      Union[float, None],
    "mlradeinangerr1":  Union[float, None],
    "mlradeinangerr2":  Union[float, None],
    "mlradeinanglim":   Union[int, None],
    "mlpmrells":        Union[float, None],
    "mlpmrellserr1":    Union[float, None],
    "mlpmrellserr2":    Union[float, None],
    "mlpmrellslim":     Union[int, None],
    "mlmodeldef":       Union[int, None],
    "plntreflink":      Union[str, None],
}


class ExoplanetMicrolensing(object):
    __slots__ = [
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "ExoplanetMicrolensing":
        return cls(data)


def _add_func(name: str):
   @property
   def fn(self) -> _ATTRS.get(name):
       if name not in self._cache:
           self._cache[name] = self._data.get(name)
       return self._cache[name]
   setattr(ExoplanetMicrolensing, name, fn)

for attr in _ATTRS:
    _add_func(attr)
