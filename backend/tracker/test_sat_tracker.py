from datetime import datetime

import pytest
import settings
from skyfield.api import EarthSatellite

from . import ts
from .sat_tracker import SatelliteTracker

# NOAA 20 (43013) TLE as of 26/11/21
line1 = "1 43013U 17073A   21329.80448036  .00000033  00000-0  36494-4 0  9995"
line2 = "2 43013  98.7360 266.0829 0000764  84.9110 275.2153 14.19562196208334"

# Use known settings
# Import settings:
#   Ground station: Melbourne
#   Min altitude: 30 degrees
settings.USE_DEFAULTS = True


@pytest.fixture
def sat() -> EarthSatellite:
    return EarthSatellite(line1, line2, "NOAA 20", ts)


def compare_dt(left: datetime, right: datetime, err: int = 1) -> bool:
    return abs((left - right).total_seconds()) <= err


class TestSatTracker():
    def test_compute_next_pass(self, sat: EarthSatellite) -> None:
        sat_tracker = SatelliteTracker()

        start = datetime(2021, 11, 26, 16)  # 4pm 26th Nov

        # NOTE: the satellite must reach an altitude of 30 degrees before the
        # pass is considered to have started.
        rt, st = sat_tracker.compute_next_pass(sat, start)

        # According to Stellarium
        rt_ = datetime(2021, 11, 27, 1, 54, 6).astimezone(sat_tracker.tz)
        st_ = datetime(2021, 11, 27, 1, 59, 16).astimezone(sat_tracker.tz)

        assert (compare_dt(rt, rt_)
                and compare_dt(st, st_))
