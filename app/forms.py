from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app import db
from app.models import User
import sqlalchemy as sa
from wtforms import TextAreaField
from wtforms.validators import Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password =  PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username== username.data))
        if user is not None:
            raise ValidationError("Please Use different User Name")
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email== email.data))
        if user is not None:
            raise ValidationError("Please Use different Email")
        
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orignal_username = original_username
    
    def validate_username(self, username):
        if username.data != self.orignal_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError("Please use a different username!")

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField("Say Something...", 
                         validators=[DataRequired(), Length(min=1, max=140)]
                         )
    submit = SubmitField("Post")
    
    