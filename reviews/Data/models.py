from datetime import datetime
from reviews import db

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return 'userId = {0}, username = {1}, password = {2}, role = {3}'.format(self.userId, self.username, self.password, self.role)

class Genre(db.Model):
    genreId = db.Column(db.String(100), primary_key=True)
    description = db.Column(db.String(50), nullable = True)

    def __repr__(self):
        return 'genreId = {0}, description = {1}'.format(self.genreId,self.description)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float, nullable = True)
    description = db.Column(db.String(20000), nullable = True)
    credibility = db.Column(db.Float, nullable = True)
    reviewAI = db.Column(db.String(10000), nullable = True)

    def __repr__(self):
        return 'gameId = {0}, title = {1}, rating = {2}, description = {3}, credibility = {4}, reviewAI = {5}'.format(self.gameId, self.title,self.rating,self.description,self.credibility,self.reviewAI)

GenreGame = db.Table('GenreGame',
    db.Column('genreId', db.String(100), db.ForeignKey('genre.genreId'), primary_key=True),
    db.Column('gameId', db.Integer, db.ForeignKey('game.gameId'), primary_key=True)
)

class Comment(db.Model):
    commmentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable = False)
    gameId = db.Column(db.Integer, db.ForeignKey('game.gameId'), nullable = False)
    content = db.Column(db.String(10000), nullable = False)
    creationDateTime = db.Column(db.DateTime, nullable = False, default=datetime.now())

    def __repr__(self):
        return '<Comment %r>' % self.commentId
        