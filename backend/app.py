from flask import Flask
from tracker.sat_tracker import SatelliteTracker


def create_app(config=None):
    app = Flask(__name__)
    if config is None:
        # app.config.from_pyfile()
        pass
    else:
        app.config.from_mapping(config)

    @app.route("/")
    @app.route("/index")
    def index():
        sat_tracker = SatelliteTracker()

        sat_tracker.add_satellite(43013)
        AOS, LOS = sat_tracker.passes[43013]
        print(AOS)
        print(LOS)

        return "<h1>Next Pass</h1><p>" + str(AOS) + "</p><p>" + str(LOS) + "</p>"

    return app
