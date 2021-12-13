import shelve

from flask import current_app, g


def get_sats_db():
    """Open a connection to the database.

    Checks whether a connection already exists for the current request and
    reuses it if possible.
    """
    if 'sats' not in g:
        g.sats = shelve.open(current_app.config['SATS_DB'])

    return g.sats


def get_passes_db():
    if 'passes' not in g:
        g.passes = shelve.open(current_app.config['PASSES_DB'])

    return g.passes


def close_db(err=None):
    """Clean up the connection to the database."""
    sats = g.pop('sats', None)
    passes = g.pop('sats', None)

    if sats is not None:
        sats.close()

    if passes is not None:
        passes.close()


def init_app(app):
    """Register database functions with the app."""
    app.teardown_appcontext(close_db)
