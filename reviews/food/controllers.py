from flask import Blueprint, render_template
from reviews.models import Item

food = Blueprint("food", __name__, template_folder="templates")

@food.route('/food')
def index():
    carousell = Item.query.filter(Item.itemType=="Food").limit(3).all()
    food = Item.query.filter(Item.itemType=="Food").all()
    return render_template("foodIndex.html", title="Index", carousell=carousell, food=food)