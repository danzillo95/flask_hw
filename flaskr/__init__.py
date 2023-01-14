import os
from flask import Flask, request, render_template
from Classes import User
from faker import Faker
from markupsafe import escape
import pandas as pd
import requests
from flaskr.db import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/tracks-sec')
    def tracks_sec():
        datbase = get_db()
        post = datbase.execute("SELECT title, lenght FROM tracks").fetchall()
        return render_template("tracks_sec.html", tracks_sec=[artist[::] for artist in post])

    @app.route('/tracks-sec/statistics')
    def tracks_sec_stat():
        datbase = get_db()
        post = datbase.execute("SELECT AVG(lenght), SUM(lenght) FROM tracks").fetchall()
        return render_template("tracks_sec_stats.html", tracks_sec_stats=[i[::] for i in post])

    @app.route("/names")
    def names():
        datbase = get_db()
        post = datbase.execute("SELECT DISTINCT artist FROM tracks").fetchall()
        return render_template("names.html", artists=[artist[0] for artist in post])

    @app.route("/tracks")
    def tracks():
        datbase = get_db()
        post = datbase.execute("SELECT title FROM tracks").fetchall()
        return render_template("tracks.html", titles=len([title[0] for title in post]))

    @app.route("/tracks/<genre>")
    def tracks2(genre):
        datbase = get_db()
        post = datbase.execute(f"SELECT title FROM tracks WHERE genre = '{escape(genre)}'").fetchall()
        return render_template("tracks2.html", titles=[title[0] for title in post])

    @app.route("/requirments/")
    def req():
        return open('requirments.txt')

    @app.route("/generate-users/", methods=['GET'])
    def generate_users():
        fake = Faker(['ja_JP'])
        return render_template(
            "generate_users.html",
            users=[User(*fake.name().split(), fake.email()) for _ in range(request.args.get("count", 100, int))]
        )

    @app.route("/mean/")
    def mean():
        df = pd.read_csv(r'hw.csv')
        heigh = df[' "Height(Inches)"'].mean()
        weight = df[' "Weight(Pounds)"'].mean()
        return f'Средний рост = {heigh}, средний вес = {weight}'

    @app.route("/space/")
    def space():
        r = requests.get('http://api.open-notify.org/astros.json')
        space_dudes = []
        for i in r.json()['people']:
            space_dudes.append(i['name'])
        return space_dudes

    return app
