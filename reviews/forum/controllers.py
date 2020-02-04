from flask import Blueprint, render_template, request
from reviews.models import Thread, Post

forum = Blueprint("forum",__name__,template_folder="templates")

@forum.route('/forum')
def index():
    threads = Thread.query.order_by(Thread.datetimeCreated.desc())
    return render_template("forum_index.html", threads = threads)
    
@forum.route('/forum/food')
def food():
    return "See more discussion abt food!"

@forum.route('/forum/games')
def games():
    return "Interested in Games huh."

