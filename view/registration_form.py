from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

import model.user as _user
import pkg.config as config
import shared

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
                shared.db, config.values["mysql"]["user_table"], username.data
                )
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = _user.get_user_by_email(
                shared.db, config.values["mysql"]["user_table"], email.data
                )
        if user is not None:
            raise ValidationError('Please use a different email address.')
