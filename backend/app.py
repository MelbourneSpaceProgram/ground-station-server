from flask import Flask
from tracker.sat_tracker import SatelliteTracker

app = Flask(__name__)


@app.route("/")
def index():
    sat_tracker = SatelliteTracker()

    sat_tracker.add_satellite(43013)
    AOS, LOS = sat_tracker.passes[43013]
    print(AOS)
    print(LOS)

    return "<h1>Next Pass</h1><p>" + str(AOS) + "</p><p>" + str(LOS) + "</p>"
