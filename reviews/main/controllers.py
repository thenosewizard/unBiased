from flask import Blueprint, render_template, flash, redirect, url_for, request
from reviews.main.forms import RegistrationForm, LoginForm, CheckReviewForm, IndexForm, genForm
from reviews.models import User, Item, Feedback, GenreItem, Comment, ItemLink, Feature
from reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user
from sqlalchemy import update
import json, requests
from itertools import zip_longest

main = Blueprint('main', __name__, template_folder= "templates")

@main.route('/', methods = ['GET', 'POST'])
def index():
    form = IndexForm()
    result = form.search(form.query.data)
    return render_template("index.html",title="Index",form=form,result=result)

@main.route('/test')
def test():
    users = User.query.all()
    return users

@main.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data,password=hashed_password,role = "Member")
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.email.data}!","success")
        return redirect(url_for('main.login'))
    return render_template("register.html",title="register",form=form)

@main.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome {user.username}!","success")
            return redirect(url_for("main.index"))
        else:
            flash("Incorrect email or password!","danger")
    return render_template("login.html",title="Login", form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/browse")
def browse():
    page = request.args.get("page", 1, type=int)
    games = Item.query.order_by(Item.rating.desc()).paginate(page= page, per_page=3)
    return render_template("browse.html", games=games)

@main.route("/review")
def review():
    index = request.args.get("index", type=int)
    item = Item.query.filter_by(itemId=index).first()
    if item == None:
        form = IndexForm()
        return redirect('main.index', title="Index", form=form)
    link = ItemLink.query.filter_by(itemId=index).first()
    pos_features = Feature.query.filter_by(itemId = index, positive = True)
    neg_features = Feature.query.filter_by(itemId = index, positive = False)
    if item.address == None:
        section = "steam"
    else:
        section = "yelp"
    requestjson = {
        "section" : section,
        "id" : str(item.refid)
    }
    reviewAI = requests.get("http://35.240.189.97/reviewGen", json = requestjson).content
    item.reviewAI = removeExtra(reviewAI)
    return render_template("review.html", item=item, link=link, pos_features=pos_features, neg_features = neg_features, zip_longest=zip_longest)

@main.route("/checkreview", methods = ['GET','POST'])
def checkreview():
    form = CheckReviewForm()
    isbiased = False
    if form.is_submitted():
        if form.validate():
            requestjson = { "review" : form.content.data }
            result = requests.get("http://35.240.189.97/classifyYelp", json = requestjson)
            if str(result.content) == 'b\'"1"\\n\'':
                isbiased = False
            else:
                isbiased = True
            print(isbiased)
            flash("Please wait while we process your review", "success")
            
            return render_template("checkreview.html", form=form , biased = isbiased)
    return render_template("checkreview.html", form=form , biased = isbiased)

@main.route("/reviewGen", methods = ['GET','POST'])
def genReview():
    form = genForm()
    if form.is_submitted():
        if form.validate():
            index = request.args.get("index", type=int)
            item = Item.query.filter_by(itemId=index).first()
            if item.address == None:
                section = "steam"
            else:
                section = "yelp"
            requestjson = {
                "section" : section,
                "id" : str(item.refid),
                "keyword" : form.content.data
            }
            review = requests.get("http://35.240.189.97/contextGen", json = requestjson)
            text = removeExtra(review.content)
            print(text)
            return render_template("textGen.html",form = form, text1 = text)
    return render_template("textGen.html",form = form, text1 = "")

def removeExtra(i):
    text = str(i)
    list = text.split("\"")
    return list[-2]

@main.route("/contacUs")
def contactUs():
    return render_template("feedback.html")

@main.route('/food')
def foodIndex():
    page = request.args.get("page", 1, type=int)
    games = Item.query.filter_by(itemType = "Food").order_by(Item.rating.desc()).paginate(page= page, per_page=3)
    return render_template("browse.html", games = games)

@main.route('/game')
def gameIndex():
    page = request.args.get("page", 1, type=int)
    games = Item.query.filter_by(itemType = "Game").order_by(Item.rating.desc()).paginate(page= page, per_page=3)
    return render_template("browse.html", games = games)

@main.route("/profile", methods = ['GET','POST'])
def profile():
    index = request.args.get('index', type=int)
    user = User.query.filter_by(id = index).first()
    if user == None:
        return redirect('main.index', title="index")
    return render_template("profile.html", user = user)

@main.route("/ban")
def ban():
    index = request.args.get('index', type=int)
    user = User.query.filter_by(id = index).first()
    if user.ban == True:
        user.ban = False
        db.session.commit()
    else:
        user.ban = True
        db.session.commit()
    print(user.ban)
    return redirect(url_for('main.profile', index = index))

@main.route("/delete")
def deleteuser():
    index = request.args.get('index', type=int)
    user = User.query.filter_by(id = index).first()
    db.session.delete(user)
    db.session.commit()
    form = IndexForm()
    return redirect(url_for('main.index', title = "index", form = form))
