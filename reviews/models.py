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
        return 'userId = {0}, username = {1}, role = {2}'.format(self.id, self.username, self.role)

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
    reviewAI = db.Column(db.String(10000), nullable = True)
    link = db.relationship('ItemLink', backref='item', lazy=True)
    image = db.Column(db.String(500), nullable = True)
    comments = db.relationship('Comment', backref = 'item', lazy = True)
    address = db.Column(db.String(500), nullable = True)
    itemType = db.Column(db.String(500), nullable = False)
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
    content = db.Column(db.String(5000))
    category = db.Column(db.String(50), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dateTimeCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship("Post", backref="Thread", lazy=True)

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.threadId, self.title, self.category, self.dateTimeCreated)

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
        #User
        User(username = 'abi', email= "abi@email.com", password = '$2b$12$HEwBRGGScKLcbQOepmjWz.OSa51kG9InyudOu/ABXU7t9RmhQGuG.', role = 'Member'),
        User(username = 'Oscar', email = "oscar@email.com", password = '$2b$12$s81hqvO2Vx0L468C8eLqP.WNnagcuqoXYDs.QqYuCekM3cgs1hsBG', role = 'Admin'),

        #Game Genres
        Genre(name = 'Adventure', description = 'Go on a Journey and Explore!'),
        Genre(name = 'Action', description = 'Stunt, Explosions & Fights!'),
        Genre(name = 'FPS', description = 'First person shooters'),
        Genre(name = 'Multiplayer', description = 'More people = More fun'),
        Genre(name = 'Co-op', description = 'Have more fun with frinds!'),
        Genre(name = 'Strategy', description = 'Big Brain Time!'),
        Genre(name = 'Singleplayer', description = 'Have fun even when alone'),
        Genre(name = 'Casual', description = 'No stress!'),
        Genre(name = 'Open World', description = 'Entire world for you to explore!'),
        Genre(name = 'RPG', description = 'Experience life as another person!'),

        #Game
        ItemLink(itemId=1, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'),
        ItemLink(itemId=2, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/8930/Sid_Meiers_Civilization_V/'),
        ItemLink(itemId=3, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/728880/Overcooked_2/'),
        ItemLink(itemId=4, platform="PC", source ="Steam", link ='https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/'),
        Item(itemId = 1, title = 'Counter-Strike: Global Offensive', refid = 1, rating = 4.37, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
            team-based action Itemplay that it pioneered when it was launched 19 years ago. CS: GO features new maps, characters, weapons, \
            and Item modes, and delivers updated versions of the classic CS content (de_dust2, etc.).', image = "cs_go.jpg", itemType = "Game"),
        Item(title = 'Civilization V', refid = 2, rating = 4.80, description = 'Create, discover, and download new player-created maps, scenarios, interfaces, and more!', 
            image = "civv.jpg", itemType = "Game"),
        Item(title = 'Overcooked! 2',refid = 3, rating = 4.37, description = 'Overcooked returns with a brand-new helping of chaotic \
            cooking action! Journey back to the Onion Kingdom and assemble your team of chefs in classic couch co-op or online play for up to \
            four players. Hold onto your aprons… it’s time to save the world again!', image = "overcooked2.jpg", itemType = "Game"),
        Item(title = 'Witcher 3', refid = 4, rating = 4.9, description = 'As war rages on throughout the Northern Realms, you take on the greatest \
            contract of your life — tracking down the Child of Prophecy, a living weapon that can alter the shape of the world.', image = "witcher3.jpg", itemType = "Game"),
        
        #Food Genres

        #Food
        Item(title = "Secret Pizza", refid = 111, rating = 4.0, description = 'With the feel of a small New York corner pizza shop, this hidden late night spot offers \
        high counters to stand and eat while people watching. Classic video games and a pinball machine are available for guests to play with, as well as two flat screen \
        TVs showing the latest sporting events.', image = 'secretpizza.jpg', address = '3708 Las Vegas Blvd S, Level 3, The Boulevard Tower, Las Vegas, NV 89109', itemType = "Food"),
        Item(title = "Earl of Sandwich", refid = 222, rating = 4.5, description = "Welcome to Earl of Sandwich® Las Vegas. Our menu pays tribute to the art of the sandwich. \
        We feature a wide variety of sandwiches on fresh-baked artisan bread, hand-tossed salads, wraps, soups and more. We maintain our brand’s exceptional taste by using \
        only the finest, freshest ingredients available for everything we serve.", image = "earlofsandwich.jpg", address = "3667 Las Vegas Blvd S, Las Vegas, NV 89109", itemType = "Food"),
        Item(title = "Gordan Ramsay Burger", refid = 333, rating = 4.0, description = "From traditional to unique burgers, the menu items at this Las Vegas restaurant use the \
        freshest, quality ingredients. Beef patties are cooked over an open flame fuelled by hard woods — Gordon Ramsay Burger is the only gourmet burger restaurant on the \
        Strip to use this method — creating a more complex and powerful flavor. In addition to juicy burgers, this popular Vegas restaurant also offers sweet potato fries \
        with vanilla powdered sugar and pork belly bao buns. Looking for some spice? The Devil Dog will do it. These all-beef dogs are simmered in devilish hot sauce, then \
        fire-kissed on the open grill.", image = "gordanramsayburger.jpg", address = "3667 S Las Vegas Blvd, Las Vegas, NV 89109", itemType = "Food"),
        Item(title = "Wicked Spoon", refid = 444, rating = 3.5, description = "A bustling culinary food hall, the Wicked Spoon delivers well-crafted original selections for \
        every appetite. With its mix of top quality, familiar staples and imaginative seasonal dishes, this Las Vegas buffet satisfies cravings and invites discovery.", 
        image = "wickedspoon.jpg", address = "The Cosmopolitan Of Las Vegas, Level 2, The Chelsea Tower, Las Vegas, NV 89109, United States", itemType = "Food"),

        Comment(userId = 1, itemId = 1, content = 'Love it'),
        Comment(userId = 2, itemId = 1, content = '10/10'),
        Thread(threadId = 1, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!",category= "Game", userId = 1),
        Thread(threadId = 2, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?", category="Food", userId = 2),
        Thread(threadId = 3, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 4, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Thread(threadId = 5, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 6, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Thread(threadId = 7, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 8, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Thread(threadId = 9, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 10, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Post(postId = 1, title = "CSGO", authorId = 2, threadId = 1, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 2, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269"),
        Post(postId = 3, title = "CSGO", authorId = 2, threadId = 1, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 4, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269"),
        Post(postId = 5, title = "CSGO", authorId = 2, threadId = 1, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 6, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269"),
        Post(postId = 7, title = "CSGO", authorId = 2, threadId = 1, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 8, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269"),
    ]
)

db.session.execute(GenreItem.insert().values(genreId = 1, itemId = 4))
db.session.execute(GenreItem.insert().values(genreId = 2, itemId = 1))
db.session.execute(GenreItem.insert().values(genreId = 2, itemId = 4))
db.session.execute(GenreItem.insert().values(genreId = 3, itemId = 1))
db.session.execute(GenreItem.insert().values(genreId = 4, itemId = 1))
db.session.execute(GenreItem.insert().values(genreId = 4, itemId = 2))
db.session.execute(GenreItem.insert().values(genreId = 4, itemId = 3))
db.session.execute(GenreItem.insert().values(genreId = 5, itemId = 1))
db.session.execute(GenreItem.insert().values(genreId = 5, itemId = 3))
db.session.execute(GenreItem.insert().values(genreId = 6, itemId = 2))
db.session.execute(GenreItem.insert().values(genreId = 7, itemId = 2))
db.session.execute(GenreItem.insert().values(genreId = 7, itemId = 3))
db.session.execute(GenreItem.insert().values(genreId = 7, itemId = 4))
db.session.execute(GenreItem.insert().values(genreId = 8, itemId = 3))
db.session.execute(GenreItem.insert().values(genreId = 9, itemId = 4))
db.session.execute(GenreItem.insert().values(genreId = 10, itemId = 4))

db.session.commit()
