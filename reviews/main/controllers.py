from flask import Blueprint, render_template, flash, redirect, url_for, request
from reviews.main.forms import RegistrationForm, LoginForm, CheckReviewForm, IndexForm, genForm
from reviews.models import User, Item, Feedback, GenreItem, Comment, ItemLink, Feature
from reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user
import json, requests

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
    game = Item.query.filter_by(itemId=index).first()
    link = ItemLink.query.filter_by(itemId=index).first()
    features = Feature.query.filter_by(itemId = index)
    if game.address == None:
        section = "steam"
    else:
        section = "yelp"
    requestjson = {
        "section" : section,
        "id" : str(game.refid)
    }
    reviewAI = requests.get("http://35.240.189.97/reviewGen", json = requestjson).content
    game.reviewAI = removeExtra(reviewAI)
    return render_template("review.html", game=game, link=link, features=features)

@main.route("/checkreview", methods = ['GET','POST'])
def checkreview():
    form = CheckReviewForm()
    isbiased = False
    if form.is_submitted():
        if form.validate():
            requestjson = { "review" : form.content.data }
            result = requests.get("http://35.240.189.97/classifyYelp", json = requestjson)
            if result.content == 1:
                isbiased = False
            else:
                isbiased = True
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
    return render_template("feedback(Updated).html")

@main.route('/food')
def foodIndex():
    carousell = Item.query.filter(Item.itemType=="Food").limit(3).all()
    food = Item.query.filter(Item.itemType=="Food").all()
    return render_template("foodIndex.html", title="Index", carousell=carousell, food=food)
