from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,PasswordField,BooleanField,ValidationError)
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea



class Postform(FlaskForm):
    title=StringField('title',validators=[DataRequired()])
    content=StringField('content',validators=[DataRequired()],widget=TextArea())
    author=StringField('author')
    slug=StringField('slug',validators=[DataRequired()])
    submit=SubmitField('submit')

class userform(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    username=StringField("Username",validators=[DataRequired()])

    email=StringField("email",validators=[DataRequired()])
    favorite_color=StringField('favorite color')
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must Match!')])
    password_hash2=PasswordField('Confirm Password', validators=[DataRequired()])
   
    submit=SubmitField('submit')

class NamerForm(FlaskForm):
    name=StringField('what is your name?',validators=[DataRequired()])
    submit=SubmitField('submit')

class passwordform(FlaskForm):
    email=StringField('what is your email?',validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit=SubmitField('submit')

class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit=SubmitField('submit')