from datetime import datetime
from reviews import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Items
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50), nullable = False)
    comments = db.relationship('Comment', backref = 'user', lazy = True)
    posts = db.relationship("Post", backref='author', lazy = True)
    threads = db.relationship("Thread", backref = "author", lazy = True)

    def __repr__(self):
        return 'userId = {0}, username = {1}, password = {2}, role = {3}'.format(self.id, self.username, self.password, self.role)

GenreItem = db.Table('GenreItem',
    db.Column('genreId', db.Integer, db.ForeignKey('genre.genreId'), primary_key = True),
    db.Column('itemId', db.Integer, db.ForeignKey('item.itemId'), primary_key = True)
)

class Genre(db.Model):
    genreId = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(50), nullable = True)

    def __repr__(self):
        return 'genreId = {0}, description = {1}'.format(self.genreId,self.description)

class Item(db.Model):
    itemId = db.Column(db.Integer, primary_key = True)
    refid = db.Column(db.Integer, nullable = True)
    title = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Float, nullable = True)
    description = db.Column(db.String(20000), nullable = True)
    credibility = db.Column(db.Float, nullable = True)
    reviewAI = db.Column(db.String(10000), nullable = True)
    link = db.relationship('ItemLink', backref='item', lazy=True)
    image = db.Column(db.String(500), nullable = True)
    comments = db.relationship('Comment', backref = 'item', lazy = True)
    map = db.Column(db.String(500), nullable = True)
    genre = db.relationship('Genre', secondary = GenreItem, lazy = 'subquery', backref = db.backref('item', lazy = True))

    def __repr__(self):
        return 'ItemId = {0}, title = {1}, rating = {2}, description = {3}, credibility = {4}, reviewAI = {5}'.format(self.itemId, self.title,self.rating,self.description,self.credibility,self.reviewAI)

class ItemLink(db.Model):
    __tablename__ = 'ItemLink'
    linkId = db.Column(db.Integer, primary_key = True)
    itemId = db.Column(db.Integer, db.ForeignKey('item.itemId'), nullable = False)
    platform = db.Column(db.String(50), nullable = False)
    source = db.Column(db.String(100), nullable = False)
    link = db.Column(db.String(1000), nullable = False)

    def __repr__(self):
        return '{}{}{}{}'.format(self.linkId, self.itemId, self.platform, self.source, self.link)

class Comment(db.Model):
    commentId = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    itemId = db.Column(db.Integer, db.ForeignKey('item.itemId'), nullable = False) 
    content = db.Column(db.String(10000), nullable = False)
    creationDateTime = db.Column(db.DateTime, nullable = False, default = datetime.now())

    def __repr__(self):
        return 'commentId = {0}, userId = {1}, itemId = {2}, content = {3}, creationDateTime = {4}'.format(self.commentId, self.userId, self.itemId, self.content, self.creationDateTime)

class Feedback(db.Model):
    feedbackId = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), nullable = False)
    name = db.Column(db.String(50), nullable = True)
    content = db.Column(db.String(1000), nullable = False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.feedbackId, self.email, self.name, self.content)

#Forum
class Thread(db.Model):
    threadId = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    category = db.Column(db.String(50), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetimeCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship("Post", backref="Thread", lazy=True)

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.threadId, self.title, self.category, self.datetimeCreated)

class Post(db.Model):
    postId = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    threadId = db.Column(db.Integer, db.ForeignKey('thread.threadId'), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    dateTimePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.postId}', '{self.title}', '{self.threadId}', '{self.dateTimePosted}')"

    

db.drop_all()

db.create_all()

db.session.add_all(
    [
        Genre(name = 'Adventure', description = 'Go on a Journey and Explore!'),
        Genre(name = 'Action', description = 'Stunt, Explosions & Fights!'),
        ItemLink(itemId=1, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=2, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=3, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=4, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=5, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=6, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=7, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=8, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=9, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=10, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=11, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=12, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=13, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=14, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=15, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'Recommend this Item to anyone who wants to take an FPS Item more competitively.\
                Item is absolutely addicting especially with a well balanced ranking system after the update and it is very cheap. A unique market \
                that have their own economy for Skins, Case keys and etc. For those who have 5 to 10 dollars to spend and havent yet buy this Item. \
                I would recommend you to buy this. :)',
                 image = "cs_go.jpg"),
        Item(title = 'Overcooked! 2', rating = 5.0, description = 'Overcooked returns with a brand-new helping of chaotic \
            cooking action! Journey back to the Onion Kingdom and assemble your team of chefs in classic couch co-op or online play for up to \
                four players. Hold onto your aprons… it’s time to save the world again!', 
                credibility = 4.0, reviewAI = 'This Item has online coop now. There are a ton of levels, different settings the map to explore \
                    is huge. There is a new throwing mechanic super fun. Levels are super dynamic, new styles like one person has to control a \
                        platform to get everyone else to a specific place. There are these like secret "Kevin" levels. Tons of new recipes, sushi \
                            and stuff. If you loved the first overcooked you will love this one. If you havent played overcooked 1, if you want a \
                                good couch coop this is the best you can get.',  image = "overcooked2.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Item(title = 'Counter-Strike: Global Offensive', rating = 5.0, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
                and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', 
                credibility = 5.0, reviewAI = 'PERFECT 10/10',  image = "cs_go.jpg"),
        Comment(userId = 1, itemId = 1, content = 'Love it'),
        Comment(userId = 2, itemId = 1, content = '10/10'),
        ItemLink(itemId = 1, platform = 'PC', source = 'Steam', link = 'www.steam.com'),
        Thread(threadId = 1, title = "What Items are worth buying?", category= "Games", userId = 1),
        Thread(threadId = 2, title = "Where to find good food?", category="Food", userId = 2),
        Post(postId = 1, title = "CSGO", authorId = 2, threadId = 1, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 2, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269")
    ]
)


db.session.execute(GenreItem.insert().values(genreId = 1, itemId = 1))
db.session.execute(GenreItem.insert().values(genreId = 2, itemId = 1))

db.session.commit()
