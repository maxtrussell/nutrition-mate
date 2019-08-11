from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db

config = Config()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    registration_key = StringField('Registration Key', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = _user.get_user_by_username(
                get_db(config), config.db.USERS, username.data
                )
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = _user.get_user_by_email(
                get_db(config), config.db.USERS, email.data
                )
        if user is not None:
            raise ValidationError('Please use a different email address.')
