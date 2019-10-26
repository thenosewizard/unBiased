from flask import Blueprint, render_template
evaluation = Blueprint('evaluation', __name__, template_folder= "templates")


@evaluation.route('/')
def index():
    return render_template('reviews_index.html')