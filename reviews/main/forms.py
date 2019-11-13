from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from reviews.Data.models import User, Game


class RegistrationForm(FlaskForm):
    # firstName = StringField('FirstName',
    #     validators=[DataRequired(), Length(min=2, max=20)])
    # lastName = StringField('LastName',
    #     validators=[DataRequired(), Length(min=2, max=20)])
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

<<<<<<< HEAD

class IndexForm(FlaskForm):
    query = StringField("Search for a game ...")
    submit = SubmitField("Search for a game")

    def search(self, query):
        if (query == None):
            query = ""
        if (query != ""):
            game = Game.query.filter(Game.title.contains(query)).all()
            return(game)
        else:
            return []
=======
class CheckReviewForm(FlaskForm):
    content = StringField("Review",
        validators=[DataRequired()])
    submit = SubmitField("Check")
>>>>>>> 8081500f9f3b5ec72745fcb6fbacce68de1cfed3
