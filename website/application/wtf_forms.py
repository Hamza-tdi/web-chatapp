from wtforms import PasswordField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *
from passlib.hash import pbkdf2_sha256


def invalid_credentials(form, field):
    """ username and password checker"""
    username = form.username.data
    password = field.data

    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValidationError('Username or Password are invalid')
    elif not pbkdf2_sha256.verify(password, user.password):
        raise ValidationError('Username or Password are invalid')


class RegistrationForm(FlaskForm):
    """ Registration Form"""

    username = StringField('username_label',
                           validators=[InputRequired(message='Usrename required'),
                                       Length(min=4, max=25, message='Username must be between 4 and 25 charachter')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required'),
                                         Length(min=8, max=64, message='Password must be between 8 and 64 charachter')])
    confirm_pswd = PasswordField('confirm_pswd_label',
                                 validators=[InputRequired(message='Password required'),
                                             Length(min=8, max=64,
                                                    message='Password must be between 8 and 64 charachter')])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User name already exist!')


class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message='Username Required')])
    password = PasswordField('password_label', validators=[InputRequired(message='Password Required'),
                                                           invalid_credentials])

    submit_button = SubmitField('Login')
