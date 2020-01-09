from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# import firebase_admin
# from firebase_admin import db

# firebase_admin.initialize_app(options={
#     'databaseURL': 'https://unbiased-ded52.firebaseio.com'
# })

# firedb = db.reference('user')
# testdata = {
#     "username":"abi.bb",
#     "email":"abi@email.com",
#     "password":"123456780",
#     "role":"Member"
# }
# firedb.push(testdata)
#here is to register you blueprints so called "modules"
app = Flask(__name__)
app.config["SECRET_KEY"] = "0b8f10037b145832e9d071f25e8b90f6"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unbiased.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from reviews.main.controllers import main
from reviews.food.controllers import food
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(food)


