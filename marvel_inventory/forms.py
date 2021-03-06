from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # email, password, submit attributes
    email = StringField('Email', validators = [DataRequired(), Email()])
    name = StringField('Name', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()