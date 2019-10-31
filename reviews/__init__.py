from flask import Flask
from reviews.main.controllers import main
from reviews.evaluation.controllers import evaluation

#here is to register you blueprints so called "modules"
app = Flask(__name__)
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(evaluation, url_prefix='/reviews')