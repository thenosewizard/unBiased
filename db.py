from flask import Flask
from reviews import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database\\unbiased.db'

db = SQLAlchemy(app)

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Genre(db.Model):
    genreId = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Genre %r>' % self.genreId

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Game %r>' % self.gameId

class Comment(db.Model):
    commmentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable=False)
    content = db.Column(db.String(9000), nullable=False)
    creationDateTime = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Comment %r>' % self.commentId
        