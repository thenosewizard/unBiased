from flask import Blueprint, render_template, request
from reviews.models import Thread, Post
from reviews import db

forum = Blueprint("forum",__name__,template_folder="templates")

@forum.route('/forum')
def index():
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.paginate(page=page, per_page=8)
    return render_template("forum_index.html", threads = threads)
    
@forum.route('/forum/food')
def food():
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.filter_by(category="Food").paginate(page=page,per_page=8)
    return render_template("forum_food.html", threads = threads)

@forum.route('/forum/game')
def game():
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.filter_by(category="Game").paginate(page=page,per_page=8)
    return render_template("forum_game.html", threads = threads)

@forum.route('/forum/thread')
def thread():
    index = request.args.get('index', type=int)
    selected_thread = Thread.query.filter_by(threadId = index).first()
    posts = Post.query.filter_by(threadId = index).paginate(per_page=8)
    return render_template('thread.html', posts=posts, thread = selected_thread)

