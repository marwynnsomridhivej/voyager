from typing import Union

from .sentrybase import SentryBase
from .sentryo import SentryDataO
from .sentryr import SentryDataR
from .sentrys import SentryDataS
from .sentrysignatures import SentrySignature
from .sentrysummary import SentrySummary
from .sentryv import SentryDataV


def _handle(pot_conv: str) -> Union[float, int, str]:
    try:
        if "." in pot_conv:
            return float(pot_conv)
        return int(pot_conv)
    except ValueError:
        return pot_conv


__all__ = [
    'SentryBase',
    'SentryDataO',
    'SentryDataR',
    'SentryDataS',
    'SentrySignature',
    'SentrySummary',
    'SentryDataV',
]


__author__ = "Marwynn Somridhivej"
__copyright__ = "Copyright 2020, Marwynn Somridhivej"
__credits__ = ["Marwynn Somridhivej"]
__license__ = 'MIT'
__version__ = 'v1.0.0-alpha.1'
__maintainer__ = "Marwynn Somridhivej"
__email__ = "msomridhivej329@gmail.com"
__status__ = "Development"
