from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, \
    FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    username = StringField(label='Username')
    password = PasswordField(label='Password')
    submit = SubmitField(label='Sign In')

