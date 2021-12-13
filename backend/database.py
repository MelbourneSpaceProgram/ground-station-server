import dbm

from flask import current_app, g


def get_db():
    """Open a connection to the database.

    Checks whether a connection already exists for the current request and
    reuses it if possible.
    """
    if 'db' not in g:
        g.db = dbm.open(current_app.config['DATABASE'], 'c')

    return g.db


def close_db(err=None):
    """Clean up the connection to the database."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialise the database from the schema."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


def init_app(app):
    """Register database functions with the app."""
    app.teardown_appcontext(close_db)
