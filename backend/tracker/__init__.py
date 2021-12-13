"""Initialisation code for the tracker module."""

import pytz
import settings
from skyfield.api import load

ts = load.timescale()
tz = pytz.timezone(settings.get("timezone"))
