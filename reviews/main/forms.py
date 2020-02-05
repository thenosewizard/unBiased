from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from reviews.models import User, Item


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField("Confirm_Password",
                                    validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is taken. Please enter a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is taken. PLease enter another email.")


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    submit = SubmitField("Login")

class IndexForm(FlaskForm):
    query = StringField("Search for a game ...")
    submit = SubmitField("Search")

    def search(self, query):
        if (query == None):
            query = ""
        if (query != "" and query != " "):
            game = Game.query.filter(Game.title.contains(query)).all()
            return(game)
        else:
            return []

class CheckReviewForm(FlaskForm):
    content = StringField("Review",
        validators=[DataRequired()])
    submit = SubmitField("Check")

class genForm(FlaskForm):
    content = StringField("Enter an attribute")
    submit = SubmitField("Check")

class threadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = RadioField("Category", choices=[("Game", "Game"), ("Food", "Food")], validators=[DataRequired()] )
    submit = SubmitField("Submit")

class postForm(FlaskForm):
    title = StringField("Title")
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")

    