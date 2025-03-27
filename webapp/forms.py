from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField,
    IntegerField, TextAreaField, SelectField, DateField
)
from wtforms.validators import (
    DataRequired, Length, Email, Regexp,
    EqualTo, ValidationError, Optional, URL
)
from webapp.models import User, Skills
import re

# -------------------- Utility Functions --------------------
def validate_password_complexity(form, field):
    password = field.data
    errors = []
    
    # Check individual requirements
    has_length = len(password) >= 8
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_number = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))
    
    # Count met criteria
    met_criteria = sum([has_lowercase, has_uppercase, has_number, has_special])
    
    # Validate each requirement
    if not has_length:
        errors.append("✗ Password must be at least 8 characters long")
    if not has_lowercase:
        errors.append("✗ Password must contain at least one lowercase letter")
    if not has_uppercase:
        errors.append("✗ Password must contain at least one uppercase letter")
    if not has_number:
        errors.append("✗ Password must contain at least one number")
    if not has_special:
        errors.append("✗ Password must contain at least one special character")
    if met_criteria < 2:
        errors.append("✗ Password must include characters from at least 2 of these categories: lowercase, uppercase, numbers, or special characters")
    
    # Calculate strength score
    strength_score = sum([
        has_length,
        has_lowercase,
        has_uppercase,
        has_number,
        has_special
    ])
    
    # Add strength feedback if there are errors
    if errors:
        strength_feedback = "Password strength: "
        if strength_score <= 2:
            strength_feedback += "Weak"
        elif strength_score <= 4:
            strength_feedback += "Medium"
        else:
            strength_feedback += "Strong"
        errors.append(strength_feedback)
    
    if errors:
        raise ValidationError(errors)
# -------------------- Authentication Forms --------------------
class RegistrationForm(FlaskForm):
    fname = StringField('First Name', 
                       validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', 
                       validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=32),
            validate_password_complexity  # Add this validator
        ]
    )
    confirm_password = PasswordField("Confirm Password", 
                                   validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username is already taken.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


# -------------------- Skills Forms --------------------
class AddForm(FlaskForm):
    title = StringField('Skill Name', validators=[DataRequired(), Length(min=2, max=25)])
    skillProg = IntegerField('Skill Progress', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_title(self, title):
        skill = Skills.query.filter_by(title=title.data, user_id=current_user.id).first()
        if skill:
            raise ValidationError("Skill already exists! Please enter a different one.")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class UpdateForm(FlaskForm):
    skillProg = IntegerField('Skill Progress', validators=[DataRequired()])
    submit = SubmitField("Update")


# -------------------- Profile Forms --------------------
class UpdateProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    bio = TextAreaField('Bio')
    resume_link = StringField('Resume Link')
    register_as = StringField('Register As')
    image_file = FileField('Update Profile Picture', 
                         validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')


# -------------------- Job Forms --------------------
class JobPostForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    type = SelectField("Job Type", 
                      choices=[
                          ("Full-time", "Full-time"),
                          ("Part-time", "Part-time"),
                          ("Remote", "Remote"),
                          ("Contract", "Contract"),
                      ], 
                      validators=[DataRequired()])
    company = StringField("Company Name", validators=[DataRequired()])
    company_url = StringField("Company Website", validators=[Optional(), URL()])
    description = TextAreaField("Job Description", validators=[DataRequired()])
    skills_required = StringField("Skills Required", validators=[DataRequired()])
    link_to_apply = StringField("Link to Apply", validators=[DataRequired(), URL()])
    deadline = DateField("Application Deadline", 
                       validators=[DataRequired()], 
                       format="%Y-%m-%d")
    submit = SubmitField("Post Job")




    