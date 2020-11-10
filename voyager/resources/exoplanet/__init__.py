# ============================
# Confirmed Planets
# ============================
from .exoplanetalias import ExoplanetAlias
from .exoplanetcomposite import ExoplanetCompositeData
from .exoplanetconfirmed import Exoplanet
from .exoplanetextended import ExoplanetExtendedData
from .exoplanetmicrolensing import ExoplanetMicrolensing
# ============================
# K2
# ============================
from .k2candidates import K2Candidate
from .k2names import K2Name
from .k2targets import K2Target
# ============================
# Kelt Time Series
# ============================
from .kelttimeseries import KELTTimeSeries
# ============================
# Kepler Objects of Interest
# ============================
from .keplerkoi import KeplerKOI
from .keplernames import KeplerNames
from .keplerstellar import KeplerStellar
from .keplertimeseries import KeplerTimeSeries
# ============================
# Mission Stars
# ============================
from .missionstars import MissionStars
# ============================
# SuperWASP Time Series
# ============================
from .superwasptimeseries import SuperWASPTimeSeries
# ============================
# Threshold Crossing Event (TCE)
# ============================
from .tce import ThresholdCrossingEvent

__all__ = [
    'ExoplanetAlias',
    'ExoplanetCompositeData',
    'Exoplanet',
    'ExoplanetExtendedData',
    'ExoplanetMicrolensing',
    'K2Candidate',
    'K2Name',
    'K2Target',
    'KELTTimeSeries',
    'KeplerKOI',
    'KeplerNames',
    'KeplerStellar',
    'KeplerTimeSeries',
    'MissionStars',
    'SuperWASPTimeSeries',
    'ThresholdCrossingEvent',
]


__author__ = "Marwynn Somridhivej"
__copyright__ = "Copyright 2020, Marwynn Somridhivej"
__credits__ = ["Marwynn Somridhivej"]
__license__ = 'MIT'
__version__ = 'v1.0.0-alpha.1'
__maintainer__ = "Marwynn Somridhivej"
__email__ = "msomridhivej329@gmail.com"
__status__ = "Development"
