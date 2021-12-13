"""This module contains the logic for tracking satellite passes."""

from datetime import datetime, timedelta
from typing import Dict, Tuple, cast

import pytz
import settings
from skyfield.api import EarthSatellite, Time, wgs84

from . import ts, tz
from .sat import Satellite


class SatelliteTracker():
    """Tracks the position of satellites and manages their events.

    Attributes:
      sats -- a dict of satellites currently being tracked using
              their NORAD ID as keys
      ts   -- Skyfield's timescale object (manages conversions
              between different timescales)
      tz   -- the timezone of the ground station
      passes   -- a dict of next passes for tracked satellites
      min_alt  -- the minimum altitude in degrees of a pass
      ground_station -- the position of the ground station
    """

    def __init__(self) -> None:
        """Init tracker with data of tracked satellites.

        Arguments:
          sats: a list of NORAD IDs
          lat: latitude of the ground station
          lon: longitude of the ground station
        """
        # Init ground station position
        lat = settings.get("lat")
        lon = settings.get("lon")
        # REVIEW: need to specify elevation?
        self.ground_station = wgs84.latlon(lat, lon)

        # Init timezone
        tz = cast(str, settings.get("timezone"))
        self.tz = pytz.timezone(tz)

        # Init min_alt
        self.min_alt = settings.get("min_alt")

        # Load satellites
        self.sats: Dict[int, Satellite] = {}
        self.passes: Dict[int, Tuple[datetime, datetime]] = {}
        for ID in settings.get("satellites"):
            ID = cast(int, ID)
            sat = Satellite(ID)
            self.sats[ID] = sat
            self.passes[ID] = self.compute_next_pass(sat.data)

        print("Loaded: " + ", ".join([str(ID) for ID in self.sats.keys()]))

    def _convert_time(self, time: datetime) -> Time:
        dt = tz.localize(time)
        return ts.from_datetime(dt)

    def _timestamp(self, time: datetime) -> str:
        dt = time.astimezone(self.tz)
        return dt.strftime("%y/%m/%d-%H:%M:%S")

    def add_satellite(self, ID: int) -> None:
        """Add satellite to tracking list."""
        sat = Satellite(ID)
        self.sats[ID] = sat
        settings.set("satellites", list(self.sats.keys()))
        self.passes[ID] = self.compute_next_pass(sat.data)

    def remove_satellite(self, ID: int) -> None:
        """Remove satellite from tracking list."""
        self.sats.pop(ID)
        settings.set("satellites", list(self.sats.keys()))

    def compute_next_pass(self, sat: EarthSatellite, t0: datetime = None,
                          t1: datetime = None) -> Tuple[datetime, datetime]:
        """Compute the times when the satellite will rise and set next."""
        start = self._convert_time(t0) if t0 is not None else ts.now()

        # REVIEW: Search over the next 24 hours (is this sufficient?)
        end = (self._convert_time(t1) if t1 is not None
               else ts.from_datetime(start.utc_datetime()
                                     + timedelta(days=1)))

        times, events = sat.find_events(self.ground_station, start, end,
                                        altitude_degrees=self.min_alt)

        # event: 0 (rise), 1 (culminate), 2 (set)
        AOS = times[next(i for i, event in enumerate(events) if event == 0)]
        LOS = times[next(i for i, event in enumerate(events) if event == 2)]

        AOS = AOS.astimezone(self.tz)
        LOS = LOS.astimezone(self.tz)

        return (AOS, LOS)

    def update(self) -> None:
        """Update satellites and check for events."""
        print("Tracking")
        for ID, (rise_t, set_t) in self.passes.items():
            print(str(ID) + ": " + self._timestamp(rise_t) + ", " +
                  self._timestamp(set_t))
