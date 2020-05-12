from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from dateutil.tz import tzlocal

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///USERS.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    hash_pass = db.Column(db.String(100))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now(tzlocal()))

    def __init__(self, first_name, last_name, email, username, avatar, hash_pass, about_me=""):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.avatar = avatar
        self.about_me = about_me
        self.hash_pass = hash_pass

    def to_dict(self):
        data = {
            'id': self.id,
            'last_seen': self.last_seen,
            'about_me': self.about_me,
            'email': self.email,
            'avatar': self.avatar,
            'username': self.username
        }
        return data


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    following_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

    def to_dict(self):

        data = {
            ""
        }