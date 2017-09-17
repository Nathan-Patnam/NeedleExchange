from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import datetime
import googlemaps
import yagmail


RADIUS = 500

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
    return app.send_static_file('createEvent.html')

@app.route('/view-event/<int:event_id>')
def view_event(event_id):
    event = Event.query.filter_by(id=event_id)[0]
    d = {
        'name': event.name,
        'organizer_name': event.organizer_name,
        'date': event.date.month + '-' + event.date.day + '-' + event.date.year,
        'time': event.date.hour + ':' + event.date.minute,
        'address': event.address,
        'phone': event.phone,
        'description': event.description,
        'email': event.email
    }
    return jsonify(d)
        

@app.route('/results')
def results():
    pass


@app.route('/signup')
def signup():
    return app.send_static_file('newUser.html')


@app.route('/signup-friend')
def signup_friend():
    pass


@app.route('/find', methods=['POST'])
def find():
    if request.method == 'POST':
        address = request.form.get('address')
        # radius = request.form.get('radius')
        event_list = []
        for event in Event.query.all():
            dist = distance(address, event.address)
            if dist <= RADIUS:
                location = gmaps.geocode(event.address)[0]['geometry']['location']
                event_list.append({'name':event.name, 'date':event.date, 'address':event.address,
                                   'lat':location['lat'], 'lng':location['lng'], 'dist':dist, 'phone':event.phone,
                                   'email':event.email, 'organizer_name':event.organizer_name})
    event_list.sort(key=lambda event: event['dist'], reverse=False)
    print (event_list)
    return jsonify(event_list)

@app.route('/create-user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        address = request.form.get('address')
        radius = RADIUS
        # radius = request.form.get('radius')
        u = User(email, address, radius)
        db.session.add(u)
        db.session.commit()
    return jsonify({"status":"ok"})

@app.route('/create-event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')

        ## FIXME
        dt = datetime.datetime(
            int(request.form.get('year')),
            int(request.form.get('month')),
            int(request.form.get('day')),
            int(request.form.get('hour')),
            int(request.form.get('minute'))
        )
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        description = request.form.get('description')
        organizer_name = request.form.get('organizer_name')
        e = Event(name, organizer_name, dt, address, description, phone=phone, email=email)
        db.session.add(e)
        db.session.commit()
        notify_users_about_event(e)
    return jsonify({"status":"ok"})


def notify_users_about_event(event):
    for user in User.query.all():
        if distance(user.address, event.address) <= RADIUS:
            notify_user(user, event)


def distance(loc1, loc2):
    distance = float(gmaps.distance_matrix(
                loc1, loc2)['rows'][0]['elements'][0]['distance']['text'].split(' ')[0].replace(',',''))
    return distance

def notify_user(user, event):
    SUBJECT = "Needle Exchange Event Near You"
    # sorry for how disgusting this is
    MESSAGE = ("You are recieving this message to notify you about a needle exchange event.\nSee below to see more information.\n\nEvent Name: %s\nOrganizer Name: %s\nDate: %s\nLocation: %s\nPhone: %s\nEmail: %s\nDescription: %s" % (event.name, event.organizer_name,str(event.date), event.address,event.phone, event.email, event.description))

    send_email(user.email, SUBJECT, MESSAGE)

def send_email(dest, subject, content):
    yag = yagmail.SMTP('NeedleXchange17@gmail.com', 'Talented17')
    contents = [content]
    yag.send(dest, subject, contents)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    organizer_name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    # days_repeat = db.Column(db.String(100))
    description = db.Column(db.Text)


    def __init__(self, name, organizer_name, date, address, description, phone=None,
                 email=None):
        self.name = name
        self.organizer_name = organizer_name
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

    def __init__(self, email, address, radius=25):
        # self.phone = phone
        self.email = email
        self.address = address
        self.radius = radius


if __name__ == '__main__':
    app.run(host='10.194.29.0', port=9000)
