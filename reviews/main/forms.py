from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    # firstName = StringField('FirstName',
    #     validators=[DataRequired(), Length(min=2, max=20)])
    # lastName = StringField('LastName',
    #     validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
        validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField("Confirm_Password",
        validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", 
        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
        validators=[DataRequired()])
    submit = SubmitField("Login")
