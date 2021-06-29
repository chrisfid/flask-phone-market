from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'That username already exists. Please choose a different one')

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError(
                'That email address already exists. Please choose a different one')

    username = StringField(label='Username:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')


class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update')

    def validate_username(self, username_to_check):
        if username_to_check.data != current_user.username:
            user = User.query.filter_by(
                username=username_to_check.data).first()
            if user:
                raise ValidationError(
                    'That username already exists. Please choose a different one')

    def validate_email_address(self, email_address_to_check):
        if email_address_to_check.data != current_user.email_address:
            email_address = User.query.filter_by(
                email_address=email_address_to_check.data).first()
            if email_address:
                raise ValidationError(
                    'That email address already exists. Please choose a different one')


class RequestResetForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField('Reset Password')
