from flask import Blueprint, render_template, flash, redirect, url_for, request
main = Blueprint('main', __name__, template_folder= "templates")
from reviews.main.forms import RegistrationForm, LoginForm, CheckReviewForm, IndexForm, genForm
from reviews.Data.models import User, Game, Feedback, GenreGame, Comment, GameLink
from reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user
# import reviews.AI.train
# import reviews.AI.getReviews
# import joblib
# import string 

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
    page = request.args.get('page', 1, type=int)
    games = Game.query.order_by(Game.rating.desc()).paginate(page= page, per_page=5)
    return render_template("browse.html", games=games)

@main.route("/review")
def review():
    index = request.args.get("index", type=int)
    game = Game.query.filter_by(gameId=index).first()
    link = GameLink.query.filter_by(gameId=index).first()
    return render_template("review.html", game=game, link=link)


@main.route("/checkreview", methods = ['GET','POST'])
def checkreview():
    form = CheckReviewForm()
    isbiased = False
    if form.is_submitted():
        if form.validate():
            review = form.content.data
            result = reviews.AI.train.predicter(review)
            print(result)
            if result == 1:
                isbiased = False
            else:
                isbiased = True
            flash("Please wait while we process your review", "success")
            return render_template("checkreview.html", form=form , biased = isbiased)
#         else:
#             flash("Please enter a review", "danger")
    return render_template("checkreview.html", form=form , biased = isbiased)



@main.route("/reviewGen", methods = ['GET','POST'])
def genReview():
    form = genForm()
    if form.is_submitted():
        if form.validate():
                text = reviews.AI.getReviews.generate_text_attr(form.content.data)
                return render_template("textGen.html",form = form, text1 =text)
    text = reviews.AI.getReviews.generate_text()
    print(text)
    return render_template("textGen.html",form = form, text1 =text)