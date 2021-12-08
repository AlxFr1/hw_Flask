import csv
from flask import Flask, url_for, Response
from faker import Faker
import requests

app = Flask(__name__)


@app.route('/')
def home():
    link_req = url_for('req')
    link_fake = url_for('fake_list', user_qty=100)
    link_mean = url_for('mean')
    link_space = url_for('space')
    return f'<p>привет, куда пойдем?</p>' \
           f'</br><a href="{link_fake}">100 поддельных личностей</a>' \
           f'</br><a href="{link_mean}">средний вес</a>' \
           f'</br><a href="{link_space}">космонавты</a>' \
           f'</br><a href="{link_req}">список зависимостей</a>'


@app.route('/requirements/')
def req():
    with open('requirements.txt', encoding="utf-8") as f:
        text = f.read().replace('\n', '<br>')
    return text


@app.route('/generate-users/<int:user_qty>/', methods=["GET"])
def fake_list(user_qty):
    fake = Faker()
    lst = [fake.name()+": "+fake.email() for _ in range(user_qty)]
    return Response("<br>".join(lst))


@app.route('/mean/')
def mean():
    height = []
    weight = []
    with open('hw.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            height += [float(row[' "Height(Inches)"']) * 2.54]
            weight += [float(row[' "Weight(Pounds)"']) * 0.454]
    mean_height = sum(height) / len(height)
    mean_weight = sum(weight) / len(weight)
    return f'средний вес = {mean_weight}, средний рост = {mean_height}'


@app.route('/space/')
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    var = r.json()["number"]
    return str(var)


if __name__ == '__main__':
    app.run()
