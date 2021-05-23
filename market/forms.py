from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
  def validate_username(self, username_to_check):
    user = User.query.filter_by(username=username_to_check.data).first()
    if user:
      raise ValidationError('That username already exists. Please choose a different one')
  
  def validate_email_address(self, email_address_to_check):
    email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
    if email_address:
      raise ValidationError('That email address already exists. Please choose a different one')

  username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
  password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
  submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
  username = StringField(label='User Name', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired()])
  submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
  
class UpdateAccountForm(FlaskForm):
  username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField(label='Update')

  def validate_username(self, username_to_check):
    if username_to_check.data != current_user.username:
      user = User.query.filter_by(username=username_to_check.data).first()
      if user:
        raise ValidationError('That username already exists. Please choose a different one')
  
  def validate_email_address(self, email_address_to_check):
    if email_address_to_check.data != current_user.email_address:
      email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
      if email_address:
        raise ValidationError('That email address already exists. Please choose a different one')

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  content = StringField('Content', validators=[DataRequired()])
  submit = SubmitField('Post')