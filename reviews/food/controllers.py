from flask import Blueprint, render_template

food = Blueprint("food", __name__, template_folder="templates")


@food.route('/food')
def index():
    return render_template("foodReview.html", title="Index")
