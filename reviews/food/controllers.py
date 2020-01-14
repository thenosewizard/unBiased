from flask import Blueprint

food = Blueprint("food",__name__, template_folder="templates")

@food.route('/food')
def index():
    return "Welcome to Food main page!"

