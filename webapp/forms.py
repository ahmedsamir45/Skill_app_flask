from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError,NumberRange
from webapp.models import User,Skills
from app import app
from flask_login import current_user


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(),Length(min=2,max=25)])
    lname = StringField('Last Name',validators=[DataRequired(),Length(min=2,max=25)])
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        # with app.app_context():
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please chosse a different one"
            )

    def validate_email(self, email):
        # with app.app_context():
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please chosse a different one")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")



class AddForm(FlaskForm):

    title = StringField('Skill Name',validators=[DataRequired(),Length(min=2,max=25)])

    skillProg = IntegerField('Skill progress',validators=[DataRequired()])

    desc = StringField('Describtion',validators=[DataRequired()])
    submit = SubmitField("ADD")

    def validate_title(self,title):
        with app.app_context():
            skill = Skills.query.filter_by(title=title.data,user_id=current_user.id).first()
        if skill:
            raise ValidationError("Skill is already exists! Please Enter a different one")
        

class DeleteForm(FlaskForm):

    
    submit = SubmitField("Delete")
   

class UpdateForm(FlaskForm):
    skillProg = IntegerField('Skill progress',validators=[DataRequired()])
    
    submit = SubmitField("Update")


        


    