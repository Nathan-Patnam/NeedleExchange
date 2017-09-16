from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import json
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyCx09A62sA9i9D3mhi392t9X_aEk74rBf4')

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'

db = SQLAlchemy(app)


@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/create')
def create_event():
    return 'hello'


@app.route('/results')
def results():
    pass


@app.route('/signup')
def signup():
    pass


@app.route('/signup-friend')
def signup_friend():
    pass


@app.route('/find', methods=['POST'])
def find():
    if request.method == 'POST':
        json_dict = request.get_json()
        print (json_dict)
        address = json_dict['address']
        radius = int(json_dict['radius'])
        for event in Event.query.all():
            distance = int(app.gmaps.distance_matrix(
                address, event.address)['rows'][0]['elements'][0]['distance']['text'].split(' ')[0])


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    days_repeat = db.Column(db.String(100))

    def __init__(self, name, date, address, phone=None,
                 email=None, days_repeat=None):
        self.name = name
        self.date = date
        self.address = address
        self.phone = phone
        self.email = email
        self.days_repeat = days_repeat


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    radius = db.Column(db.Integer)

    def __init__(self, phone, email, zipcode, radius=15):
        self.phone = phone
        self.email = email
        self.zipcode = zipcode
        self.radius = radius


if __name__ == '__main__':
    app.run(host='10.194.29.0', port=9000)
