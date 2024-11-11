from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class EmployeeForm(FlaskForm):
    first_name = StringField('First name', [DataRequired(), validators.Length(min=2, max=70), validators.Regexp('^[a-zA-Z\- ]+$', message='First name must only contain alphabetic characters and hyphens')])
    last_name = StringField('Last name', [DataRequired(), validators.Length(min=1, max=70), validators.Regexp('^[a-zA-Z\- ]+$', message='Last name must only contain alphabetic characters hyphens')])
    email = EmailField('Email', [DataRequired()])
    team_name = StringField('Team Name', [DataRequired(), validators.Length(min=3, max=30), validators.Regexp('^[a-zA-Z\- ]+$', message='Team name must only contain alphabetic characters hyphens')])
    role = StringField('Role', [DataRequired(), validators.Length(min=4, max=30), validators.Regexp('^[a-zA-Z ]+$', message='Role must only contain alphabetic characters')])
    location = SelectField('Location',[InputRequired()], choices=[('Please Select','Please Select'), ('Germany', 'Germany'), ('India', 'India'), ('Poland', 'Poland'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States')])
    date_joined = DateField('Date Joined', [InputRequired()])

    def validate_location(self, field):
        if field.data == 'Please Select':
            raise ValidationError('Please select a location')