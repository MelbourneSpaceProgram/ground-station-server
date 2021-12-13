"""Backend for the ground station.

Manages satellites, computes passes and stores observations.
"""

import os

from flask import Flask


def create_app(config=None):
    """Perform set up for the backend."""
    app = Flask(__name__,
                instance_relative_config=True)

    app.config['DATABASE'] = os.path.join(app.instance_path,
                                          'ground-station.db')

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
        pass
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return "<h1>Hello there!</h1>"

    from . import database
    database.init_app(app)

    return app
