from flask import Blueprint, render_template, flash, redirect, url_for
main = Blueprint('main', __name__, template_folder= "templates")
from reviews.main.forms import RegistrationForm, LoginForm, CheckReviewForm
from reviews.Data.models import User, Game, Feedback, GenreGame, Comment
from reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user



@main.route('/')
def index():
    return render_template('index.html')

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

@main.route("/checkreview", methods = ['GET','POST'])
def checkreview():
    form = CheckReviewForm()
    isbiased = None
    if form.is_submitted():
        if form.validate():
            flash("Please wait while we process your review", "success")
            
        else:
            flash("Please enter a review", "danger")
    return render_template("checkreview.html", form=form, isbiased=isbiased)