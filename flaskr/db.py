import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g = special object used to store data that can be accessed multiple times during a connection
# connection is stored and reused in this manner

# current_app = object that refers to current Flask object (we're using factory method so there is no canonical flask instance)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
	    # Row function accesses row that behaves like dict (columns)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    # checks if g was set (db connection was created)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # open_resource opens file relative to current directory
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# define command line command that opens database
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# init_db functions need to be registered with app if they are to be used
# since we're using factory, we don't have an instance to reference for this
# so just pass in an app as a param
# we will then call this from the __init__.py entry script
def init_app(app):
    # tells flask to call the passed in function when cleaning up after the response
    app.teardown_appcontext(close_db)
    # adds passed in function as a command line command
    app.cli.add_command(init_db_command)
