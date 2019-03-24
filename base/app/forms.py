from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, IntegerField, DateField, SelectField, SelectMultipleField, FloatField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Required
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from app.models import *
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Please enter a Username', validators=[DataRequired()])
    usertype = SelectField('What is your User Type', choices=[('Public','Public'), ('Public Service','Public Service')])
    nric = StringField('What is your NRIC?', validators=[DataRequired()])
    password = PasswordField('Please enter Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

####################### Answer forms ################################

class Boolean(FlaskForm):
    options = RadioField('Yes or No?',choices = [('yes','Yes'),('no','No')])
    submit = SubmitField('Submit')

class FreeTxt(FlaskForm):
    options = StringField('Answer', widget=TextArea(),validators=[DataRequired()])
    submit = SubmitField('Submit')

####################### Question forms #############################

class YesNoQuestion(FlaskForm):
    title = StringField('Question',validators=[DataRequired()])
    submit = SubmitField('Submit')

class OpenEndedQuestion(FlaskForm):
    title = StringField('Question',validators=[DataRequired()])
    submit = SubmitField('Submit')
