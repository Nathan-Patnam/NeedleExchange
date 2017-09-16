from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import datetime
import googlemaps
import yagmail


gmaps = googlemaps.Client(key='AIzaSyCx09A62sA9i9D3mhi392t9X_aEk74rBf4')

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
CORS(app)

db = SQLAlchemy(app)


@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/make-event')
def make_event():
    return 'hello'

@app.route('/view-event/<int:event_id>')
def view_event(event_id):
    event = Event.query.filter_by(id=event_id)[0]
    d = {
        'name': event.name,
        'date': event.date.month + '-' + event.date.day + '-' + event.date.year,
        'time': event.date.hour + ':' + event.date.minute,
        'address': event.address,
        'phone': event.phone,
        'email': event.email
    }
    return jsonify(d)
        

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
        address = request.form.get('address')
        radius = request.form.get('radius')
        event_list = []
        for event in Event.query.all():
            if distance_in_radius(address, event.address, radius):
                event_list.append({'name':event.name, 'date':event.date, 'address':event.address})
    print (event_list)
    return jsonify(event_list)

@app.route('/create-user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        address = request.form.get('address')
        radius = request.form.get('radius')
        u = User(email, address, radius)
        db.session.add(u)
        db.commit()

@app.route('/create-event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')

        ## FIXME
        dt = datetime.datetime(
            request.form.get('year'),
            request.form.get('month'),
            request.form.get('day'),
            request.form.get('hour'),
            request.form.get('minute')
        )
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        days_repeat = request.form.get('repeat')
        description = request.form.get('description')
        e = Event(name, dt, address, description, phone=phone, email=email, days_repeat=days_repeat)
        db.session.add(e)
        db.commit()
        notify_users_about_event(e)


def notify_users_about_event(event):
    for user in User.query.all():
        if distance_in_radius(user.address, event.address, user.radius):
            notify_user(user, event)


def distance_in_radius(loc1, loc2, radius):
    distance = float(gmaps.distance_matrix(
                loc1, loc2)['rows'][0]['elements'][0]['distance']['text'].split(' ')[0].replace(',',''))
    return distance < float(radius)

def notify_user(user, event):
    SUBJECT = "Needle Exchange Event Near You"
    MESSAGE = ("""
    You are recieving this message to notify you about a needle exchange event. 
    Click the link below to see more information.


    www.needlexchange.com/view-event/""" + str(event.id) +
               "\n\n\nDebug Link: 10.194.29.0:9000/view-event/" + str(event.id))
    send_email(user.email, SUBJECT, MESSAGE)

def send_email(dest, subject, content):
    yag = yagmail.SMTP('NeedleXchange17@gmail.com', 'Talented17')
    contents = [content]
    yag.send(dest, subject, contents)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    # days_repeat = db.Column(db.String(100))
    description = db.Column(db.Text)


    def __init__(self, name, date, address, description, phone=None,
                 email=None):
        self.name = name
        self.date = date
        self.address = address
        self.phone = phone
        self.email = email
        # self.days_repeat = days_repeat
        self.description = description


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    radius = db.Column(db.Integer)

    def __init__(self, email, address, radius=15):
        # self.phone = phone
        self.email = email
        self.address = address
        self.radius = radius


if __name__ == '__main__':
    app.run(host='10.194.29.0', port=9000)
