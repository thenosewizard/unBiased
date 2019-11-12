from flask import Flask
from reviews.main.controllers import main
from reviews.evaluation.controllers import evaluation

#here is to register you blueprints so called "modules"
app = Flask(__name__)
app.config["SECRET_KEY"] = "0b8f10037b145832e9d071f25e8b90f6"
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(evaluation, url_prefix='/reviews')