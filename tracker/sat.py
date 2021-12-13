"""This module contains classes that store satellite data."""

from settings import get_tle_dir
from skyfield.api import load

from . import ts


class Satellite():
    """Wrapper around Skyfield's EarthSatellite.

    Attributes:
      ID   -- the NORAD ID of the satellite
      name -- the name of the satellite
      data -- the loaded EarthSatellite object
    """

    def __init__(self, ID: int) -> None:
        """Init satellite with a name and ID.

        Checks whether the TLE is up to date and redownloads if necessary. TLEs
        are stored in a folder in the root directory.
        """
        self.ID = ID

        url = f'https://celestrak.com/satcat/tle.php?CATNR={ID}'
        filename = get_tle_dir() / f'{ID}.txt'
        self.data = load.tle_file(url, filename=filename.as_posix())[0]

        if not self.data:
            # REVIEW: what to do if loading TLE fails?
            raise Exception("Failed to load TLE for " + str(ID))

        # Check if the TLE is out of date
        if abs(ts.now() - self.data.epoch) > 14:
            self.data = load.tle_file(url, filename=filename.as_posix(),
                                      reload=True)[0]

        self.name = self.data.name
