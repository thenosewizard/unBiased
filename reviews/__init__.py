from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#here is to register you blueprints so called "modules"
app = Flask(__name__)
app.config["SECRET_KEY"] = "0b8f10037b145832e9d071f25e8b90f6"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unbiased.db'

db = SQLAlchemy(app)

from reviews.main.controllers import main
from reviews.evaluation.controllers import evaluation
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(evaluation, url_prefix='/reviews')