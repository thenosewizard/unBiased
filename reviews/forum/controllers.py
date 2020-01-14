from flask import Blueprint, render_template

forum = Blueprint("forum",__name__,template_folder="templates")

@forum.route('/forum')
def index():
    return render_template("forum_layout.html")
    
@forum.route('/forum/food')
def food():
    return "See more discussion abt food!"

@forum.route('/forum/games')
def games():
    return "Interested in Games huh."

