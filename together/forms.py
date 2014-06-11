from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, email, Required, EqualTo, ValidationError, \
    Regexp
from together.models import User


class LoginForm(Form):
    email = EmailField('Email', validators=[Required(), email()])
    password = PasswordField('Password', validators=[Required()])


class RegisterForm(Form):
    name = TextField('Name', validators=[Required(), Length(max=255), Regexp(r'^[\w]+$')])
    email = EmailField('Email', validators=[Required(), email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[Required()])

    def validate_email(self, field):
        emails = User.query.filter_by(email=field.data).all()
        if len(emails) > 0:
            raise ValidationError('This email is already in use.')

    def validate_name(self, field):
        names = User.query.filter_by(name=field.data).all()
        if len(names) > 0:
            raise ValidationError('This name is already in use.')
