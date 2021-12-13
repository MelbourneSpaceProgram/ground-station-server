"""Track satellite position and passes."""

import os
from datetime import timedelta

import pytz
from skyfield.api import load, wgs84

ts = load.timescale()
tz = pytz.timezone("Australia/Melbourne")

lat = -37.814
lon = 144.96332
elev = 0
alt = 30

ground_station = wgs84.latlon(lat, lon, elev)


def _convert_time(time):
    dt = tz.localize(time)
    return ts.from_datetime(dt)


def _timestamp(time):
    dt = time.astimezone(tz)
    return dt.strftime("%y/%m/%d-%H:%M:%S")


def _load_tle(sat_id):
    url = f'https://celestrak.com/satcat/tle.php?CATNR={sat_id}'
    filename = os.path.join("/app/data", f'{sat_id}.txt')
    sat = load.tle_file(url, filename=filename)[0]

    if not sat:
        raise Exception("Failed to load TLE for" + sat_id)

    if abs(ts.now() - sat.epoch) > 14:
        sat = load.tle_file(url, filename=filename, reload=True)[0]

    return sat


def compute_next_pass(sat_id, t0=None, t1=None):
    sat = _load_tle(sat_id)

    start = _convert_time(t0) if t0 is not None else ts.now()
    end = (_convert_time(t1) if t1 is not None
           else ts.from_datetime(start.utc_datetime() + timedelta(days=1)))

    times, events = sat.find_events(ground_station, start, end,
                                    altitude_degrees=alt)

    # event: 0 (rise), 1 (culminate), 2 (set)
    AOS = times[next(i for i, event in enumerate(events) if event == 0)]
    LOS = times[next(i for i, event in enumerate(events) if event == 2)]

    AOS = AOS.astimezone(tz)
    LOS = LOS.astimezone(tz)

    return {"AOS": _timestamp(AOS), "LOS": _timestamp(LOS)}
