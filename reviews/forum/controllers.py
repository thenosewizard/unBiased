from flask import Blueprint, render_template, request, flash, redirect, url_for
from reviews.models import Thread, Post
from reviews.main.forms import threadForm, postForm
from reviews import db
from flask_login import current_user, login_required

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
    return render_template("forum_items.html", threads = threads, title = "Food")

@forum.route('/forum/game')
def game():
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.filter_by(category="Game").paginate(page=page,per_page=8)
    return render_template("forum_items.html", threads = threads, title = "Games")

@forum.route('/forum/thread/<int:index>')
def thread(index):
    page = request.args.get('page', 1, type=int)
    selected_thread = Thread.query.filter_by(threadId = index).first()
    posts = Post.query.filter_by(threadId = index).paginate(page=page, per_page=2)
    return render_template('thread.html', posts=posts, thread = selected_thread)

@forum.route('/forum/newPost', methods=["GET","POST"])
@login_required
def newPost():
    index = request.args.get("index", type=int)
    if current_user.ban == True:
        return redirect('forum.thread', index=index)
    form = postForm()
    if form.validate_on_submit():
        newPost = Post(title = form.title.data, authorId = current_user.id, threadId = index, content=form.content.data)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("forum.thread", index=index))
    
    return render_template("newPost.html", form=form, index=index)

@forum.errorhandler(401)
def page_not_found(e):
    flash("Login Required!","danger")
    return redirect(url_for("main.login"))

@forum.route('/forum/newThread', methods=["GET","POST"])
@login_required
def newThread():
    if current_user.ban == True:
        threads = Thread.query.paginate(page=page, per_page=8)
        return redirect('forum.index', threads=threads)
    form = threadForm()
    if form.validate_on_submit():
        newThread = Thread(title = form.title.data, content = form.content.data, category = form.category.data, userId = current_user.id)
        db.session.add(newThread)
        db.session.commit()
        return redirect(url_for("forum.food"))
    
    return render_template("newThread.html", form=form)
