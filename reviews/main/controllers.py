from flask import Blueprint, render_template, flash, redirect, url_for
from reviews.main.forms import RegistrationForm, LoginForm
main = Blueprint('main', __name__, template_folder= "templates")


@main.route('/')
def index():
    return render_template('index.html')


@main.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.email.data}!","success")
        return redirect(url_for('main.login'))   
    return render_template("register.html",title="register",form=form)

@main.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "Email@email.com" and form.password.data == "12345678":
            flash(f"Welcome, {form.email.data}!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Incorrect email or password!","danger")
    return render_template("login.html",title="Login", form=form)