from flask import Flask, request
from faker import Faker
import pandas as pd
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World?</p>"


@app.route("/requirments/")
def req():
    return open('requirments.txt')


@app.route("/generate-users/", methods=['GET'])
def gen():
    count = request.args.get('count')
    res = []
    fake = Faker(['ja_JP'])
    for _ in range(int(count)):
        res.append(f'{fake.name()}, {fake.email()}')
    return res


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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
