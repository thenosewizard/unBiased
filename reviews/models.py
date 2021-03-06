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
    ban = db.Column(db.Boolean, nullable = False)

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

class Feature(db.Model):
    featureId = db.Column(db.Integer, primary_key = True)
    itemId = db.Column(db.Integer, db.ForeignKey('item.itemId'), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    positive = db.Column(db.Boolean, nullable = False)

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
        User(username = 'abi', email= "abi@email.com", password = '$2b$12$HEwBRGGScKLcbQOepmjWz.OSa51kG9InyudOu/ABXU7t9RmhQGuG.', role = 'Member', ban = False),
        User(username = 'Oscar', email = "oscar@email.com", password = '$2b$12$s81hqvO2Vx0L468C8eLqP.WNnagcuqoXYDs.QqYuCekM3cgs1hsBG', role = 'Admin',ban = False),
        User(username = "Zach", email= "Zach@email.com", password='$2b$12$HEwBRGGScKLcbQOepmjWz.OSa51kG9InyudOu/ABXU7t9RmhQGuG.', role = 'Member',ban = False),

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
        Item(title = 'Counter-Strike: Global Offensive', refid = 1, rating = 4.37, description = 'Counter-Strike: Global Offensive (CS: GO) expands upon the \
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
        Genre(name = "American", description = "Classic American food"),
        Genre(name = "Vegetarian Option", description = "For vegetarians"),
        Genre(name = "Wifi", description = "Who doesn't want free wifi?"),

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

        #Feature
        Feature(itemId = 5, description = "late night", positive = True),
        Feature(itemId = 5, description = "pizza delicious", positive = True),
        Feature(itemId = 5, description = "3rd Floor", positive = True),
        Feature(itemId = 5, description = "Hidden Gem", positive = True),
        Feature(itemId = 5, description = "Last Bubble Gum on the floor", positive = True),
        Feature(itemId = 5, description = "'Las Vegas", positive = True),
        Feature(itemId = 5, description = "White pizza", positive = True),
        Feature(itemId = 5, description = "secret pizza", positive = True),
        Feature(itemId = 5, description = "best pizza", positive = True),
        Feature(itemId = 5, description = "really good", positive = True),

        Feature(itemId = 5, description = "customer service", positive = False),
        Feature(itemId = 5, description = "excited try", positive = False),
        Feature(itemId = 5, description = "line hour", positive = False),
        Feature(itemId = 5, description = "place sucks", positive = False),
        Feature(itemId = 5, description = "pizza terrible", positive = False),
        Feature(itemId = 5, description = "'tasted like", positive = False),
        Feature(itemId = 5, description = "average pizza", positive = False),
        Feature(itemId = 5, description = "'pizza ok", positive = False),
        Feature(itemId = 5, description = "'pizza average", positive = False),

        Feature(itemId = 6, description = "great sandwiches", positive = True),
        Feature(itemId = 6, description = "time vegas", positive = True),
        Feature(itemId = 6, description = "good sandwich", positive = True),
        Feature(itemId = 6, description = "24 hours", positive = True),
        Feature(itemId = 6, description = "earl club", positive = True),
        Feature(itemId = 6, description = "italian sandwich", positive = True),
        Feature(itemId = 6, description = "really good", positive = True),
        Feature(itemId = 6, description = "best sandwich", positive = True),
        Feature(itemId = 6, description = "tuna melt", positive = True),
        Feature(itemId = 6, description = "planet hollywood", positive = True),

        Feature(itemId = 6, description = "don understand", positive = False),
        Feature(itemId = 6, description = "understand hype", positive = False),
        Feature(itemId = 6, description = "tasted like", positive = False),
        Feature(itemId = 6, description = "order wrong", positive = False),
        Feature(itemId = 6, description = "small sandwiches", positive = False),
        Feature(itemId = 6, description = "'yelp let", positive = False),
        Feature(itemId = 6, description = "gross gross", positive = False),
        Feature(itemId = 6, description = "got food", positive = False),
        Feature(itemId = 6, description = "just ok", positive = False),

        Feature(itemId = 7, description = "burger amazing", positive = True),
        Feature(itemId = 7, description = "farm burger", positive = True),
        Feature(itemId = 7, description = "truffle fries", positive = True),
        Feature(itemId = 7, description = "planet hollywood", positive = True),
        Feature(itemId = 7, description = "euro burger", positive = True),
        Feature(itemId = 7, description = "highly recommend", positive = True),
        Feature(itemId = 7, description = "really good", positive = True),
        Feature(itemId = 7, description = "best burgers", positive = True),
        Feature(itemId = 7, description = "burger delicious", positive = True),
        Feature(itemId = 7, description = "best burger", positive = True),

        Feature(itemId = 7, description = "fries cold", positive = False),
        Feature(itemId = 7, description = "save money", positive = False),
        Feature(itemId = 7, description = "food poisoning", positive = False),
        Feature(itemId = 7, description = "fries soggy", positive = False),
        Feature(itemId = 7, description = "way better", positive = False),
        Feature(itemId = 7, description = "tasted like", positive = False),
        Feature(itemId = 7, description = "mediocre best", positive = False),
        Feature(itemId = 7, description = "waste time", positive = False),
        Feature(itemId = 7, description = "ordered medium", positive = False),

        Feature(itemId = 8, description = "definitely come", positive = True),
        Feature(itemId = 8, description = "good buffet", positive = True),
        Feature(itemId = 8, description = "pretty good", positive = True),
        Feature(itemId = 8, description = "great buffet", positive = True),
        Feature(itemId = 8, description = "bone marrow", positive = True),
        Feature(itemId = 8, description = "favorite buffet", positive = True),
        Feature(itemId = 8, description = "french toast", positive = True),
        Feature(itemId = 8, description = "wicked spoon", positive = True),
        Feature(itemId = 8, description = "really good", positive = True),
        Feature(itemId = 8, description = "best buffet", positive = True),

        Feature(itemId = 8, description = "food poisoning", positive = False),
        Feature(itemId = 8, description = "save money", positive = False),
        Feature(itemId = 8, description = "worst buffet", positive = False),
        Feature(itemId = 8, description = "food mediocre", positive = False),
        Feature(itemId = 8, description = "food cold", positive = False),
        Feature(itemId = 8, description = "tasted like", positive = False),
        Feature(itemId = 8, description = "good thing", positive = False),
        Feature(itemId = 8, description = "food just", positive = False),
        Feature(itemId = 8, description = "waste money", positive = False),

        Comment(userId = 1, itemId = 1, content = 'Love it'),
        Comment(userId = 2, itemId = 1, content = '10/10'),
        Thread(threadId = 1, title = "CSGO VAC BAN by bot called ZONERBOT.xyz", content="Hello, I recently received a vac ban I must've been \
            mistook for someone else because I've never cheated. That is the last thing on my mind, I've played with cheaters before but I've \
                always made sure to report them and I've overwatched several cases. I'm totally against cheating, this came as a big surprise.",
                category= "Game", userId = 1),
        Thread(threadId = 2, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?", category="Food", userId = 2),
        Thread(threadId = 3, title = "Looking for the Title of this MMO!", content="I recently came across a free MMO survival sandbox game (or \
            so the description seemed to explain it that way). Where you make an undead character in avast desert like region. You are able to \
                craft housing and material. I don't believe there is a leveling system, or that I saw. There is use of magic, black magic \
                    combinations, and other item crafts. I did not add the game to my wishlist or got the title of it...but I know it starts with\
                    'Armi---or Irma....' something with an 'A' or 'I'", category= "Game", userId = 1),
        Thread(threadId = 4, title = "What did you just eat?", content="It could be breakfast, lunch, dinner or a quick snack.",  category="Food", userId = 2),
        Thread(threadId = 5, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 6, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Thread(threadId = 7, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 8, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Thread(threadId = 9, title = "What games are worth buying?", content="I don't know what games to play on Steam. Help Please!", category= "Game", userId = 1),
        Thread(threadId = 10, title = "Where to find good food?", content="Hi guys! I want to know where can I eat good food in Singapore. Any \
             Suggestions?",  category="Food", userId = 2),
        Post(postId = 1, title = "CSGO", authorId = 2, threadId = 1, content = "Report bots do not give vac. Report bots do not even work."),
        Post(postId = 2, authorId = 1, threadId = 2, content = "Chomp Chomp has the best food! Its at 20 Kensington Park Rd, Singapore 557269"),
        Post(postId = 3, title = "CSGO", authorId = 1, threadId = 1, content = "That's not an answer. Thanks anyway"),
        Post(postId = 4, authorId = 1, threadId = 4, content = "I just had a small salad and a grilled chicken sandwich. Boring, but healthy."),
        Post(postId = 5, title = "CSGO", authorId = 3, threadId = 1, content = "hes right tho, report bots can at best get you into overwatch, which wont ban you if legit. i would know im banned"),
        Post(postId = 6, authorId = 3, threadId = 4, content = "6oz of shredded chicken."),
        Post(postId = 7, title = "CSGO", authorId = 2, threadId = 5, content = "I will recommend you to try CSGO. Its really fun!"),
        Post(postId = 8, authorId = 3, threadId = 4, content = "BBQ beans with cornbread and celery with ranch. Enjoyed it with my son at school. He only liked the cornbread:/"),
        Post(postId = 9, title = "Inferna", authorId = 2, threadId = 3, content = "Maybe Inferna?"),
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
db.session.execute(GenreItem.insert().values(genreId = 11, itemId = 5))
db.session.execute(GenreItem.insert().values(genreId = 11, itemId = 6))
db.session.execute(GenreItem.insert().values(genreId = 11, itemId = 7))
db.session.execute(GenreItem.insert().values(genreId = 11, itemId = 8))
db.session.execute(GenreItem.insert().values(genreId = 12, itemId = 5))
db.session.execute(GenreItem.insert().values(genreId = 12, itemId = 6))
db.session.execute(GenreItem.insert().values(genreId = 12, itemId = 7))
db.session.execute(GenreItem.insert().values(genreId = 12, itemId = 8))
db.session.execute(GenreItem.insert().values(genreId = 13, itemId = 6))
db.session.execute(GenreItem.insert().values(genreId = 13, itemId = 7))

db.session.commit()
