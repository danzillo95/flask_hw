import sqlite3
import click
from flask import current_app, g
import csv


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    file = open('flaskr/tracks.csv')
    contents = csv.reader(file)
    res = [(tuple(line)) for line in contents]
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.execute(
        f"""
        INSERT INTO tracks (title, artist, genre, lenght) VALUES {str(res[1::])[1:-1]}
        """
    )
    db.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
