from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import validators, StringField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, InputRequired, ValidationError

from app.models.user import User


class RegistrationForm(FlaskForm):
    account_type = RadioField('Select Account Type:',[InputRequired()], choices=[('admin','Admin'),('regular','Regular')])
    email = EmailField('Email', [DataRequired()])
    first_name = StringField('First Name', [DataRequired(), validators.Length(min=2, max=15), validators.Regexp('^[A-Za-z]+$', message='First name must only contain alphabetic characters')])
    password = PasswordField('Password', [DataRequired(), validators.Length(min=7, max=20), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), validators.EqualTo('password', message='Passwords do not match')])

class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError('Incorrect password')