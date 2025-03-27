
from webapp.models import User
from flask import render_template ,url_for,flash ,redirect,request
from webapp.forms import RegistrationForm , LoginForm,UpdateProfileForm
from webapp import bcrypt,db
from flask_login import login_user,current_user,logout_user
from flask import Blueprint
from flask_login import current_user,login_required

auth_pages = Blueprint("auth_pages",__name__)



@auth_pages.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_pages.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create a new user with all fields
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password
        )
        
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        
        # Flash a success message
        flash(f"Account created successfully for {form.username.data}", "success")
        
        # Redirect to the login page
        return redirect(url_for("auth_pages.login"))
    
    # Render the registration form
    return render_template("register.html", title="Register", form=form ,custom='auth')

@auth_pages.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_pages.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password , form.password.data)):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("auth_pages.dashboard"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form,custom="auth")

@auth_pages.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main_pages.home"))






from flask import request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
import time


from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from datetime import datetime
from .models import User, Jobs, db
from .forms import UpdateProfileForm, JobPostForm  # Ensure both forms are imported


from werkzeug.utils import secure_filename
import os
import base64
import io
from PIL import Image
import os
import time
import base64
import io
import re
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
@auth_pages.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    profile_form = UpdateProfileForm()
    job_form = JobPostForm()

    # Handle profile update
    if 'submit_profile' in request.form and profile_form.validate_on_submit():
        try:
            # Image processing variables
            image_folder = os.path.join(auth_pages.root_path, 'static', 'profile_pics')
            os.makedirs(image_folder, exist_ok=True)
            
            # Handling image upload
            filename = current_user.image_file  # Default to existing filename
            
            # Check for cropped image or file upload
            cropped_image_data = request.form.get("cropped_image")
            file_upload = profile_form.image_file.data

            if cropped_image_data or file_upload:
                # Generate unique filename
                ext = os.path.splitext(file_upload.filename)[1] if file_upload else '.jpg'
                filename = secure_filename(f"user_{current_user.id}_{int(time.time())}{ext}")
                image_path = os.path.join(image_folder, filename)

                # Delete old image if exists and isn't default
                if current_user.image_file and current_user.image_file != 'default/default.png':
                    old_path = os.path.join(image_folder, current_user.image_file)
                    try:
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    except Exception as e:
                        auth_pages.logger.error(f"Error deleting old image: {e}")
                        flash("Error removing old profile image", "warning")

                # Process cropped image
                if cropped_image_data:
                    try:
                        # Extract base64 data
                        if 'base64,' in cropped_image_data:
                            header, image_data = cropped_image_data.split('base64,', 1)
                        else:
                            image_data = cropped_image_data
                        
                        # Decode and save
                        image_bytes = base64.b64decode(image_data)
                        with Image.open(io.BytesIO(image_bytes)) as img:
                            if img.mode in ('RGBA', 'P'):
                                img = img.convert('RGB')
                            img.save(image_path, quality=95)
                    except Exception as e:
                        auth_pages.logger.error(f"Error processing cropped image: {e}")
                        flash("Error processing image upload", "danger")
                        return redirect(url_for('auth_pages.dashboard'))
                
                # Process file upload
                elif file_upload:
                    file_upload.save(image_path)

            # If no existing image, set to default
            if not filename:
                filename = "default/default.png"

            # Update user profile
            current_user.image_file = filename
            current_user.fname = profile_form.fname.data
            current_user.lname = profile_form.lname.data
            current_user.phone_number = profile_form.phone_number.data
            current_user.bio = profile_form.bio.data
            current_user.resume_link = profile_form.resume_link.data
            current_user.register_as = request.form.get('register_as', current_user.register_as)
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth_pages.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            auth_pages.logger.error(f"Error updating profile: {e}")
            flash('An error occurred while updating your profile', 'danger')
            return redirect(url_for('auth_pages.dashboard'))

    # Handle job posting
    elif 'submit_job' in request.form:
        # Check if form is actually validating
        if not job_form.validate_on_submit():
            flash(f"Form validation failed: {job_form.errors}", "danger")
            return redirect(url_for("auth_pages.dashboard"))

        try:
            from bs4 import BeautifulSoup

            description = job_form.description.data or ''
            soup = BeautifulSoup(description, 'html.parser')

            # Allow only safe HTML tags
            allowed_tags = ['p', 'h1', 'h2', 'h3', 'strong', 'em', 'u', 's', 'ul', 'ol', 'li', 'a', 'blockquote']
            for tag in soup.find_all(True):
                if tag.name not in allowed_tags:
                    tag.unwrap()

            # Create new job post
            job = Jobs(
                title=job_form.title.data,
                type=job_form.type.data,
                company=job_form.company.data,
                company_url=job_form.company_url.data,
                description=str(soup) if soup else '',
                skills_required=job_form.skills_required.data,
                link_to_apply=job_form.link_to_apply.data,
                deadline=job_form.deadline.data,
                posted_by_id=current_user.id
            )

            db.session.add(job)
            db.session.commit()

            flash("Job posted successfully!", "success")
            return redirect(url_for("auth_pages.dashboard"))

        except Exception as e:
            db.session.rollback()
            auth_pages.logger.error(f"Error posting job: {e}")
            flash(f"Error posting job: {str(e)}", "danger")
            return redirect(url_for("auth_pages.dashboard"))

    # Pre-populate profile form fields on GET request
    if request.method == 'GET':
        profile_form.fname.data = current_user.fname
        profile_form.lname.data = current_user.lname
        profile_form.phone_number.data = current_user.phone_number
        profile_form.bio.data = current_user.bio
        profile_form.resume_link.data = current_user.resume_link

    # Fetch data for dashboard
    skills = current_user.skills if current_user.register_as == 'employee' else []
    posted_jobs = Jobs.query.filter_by(posted_by_id=current_user.id).order_by(Jobs.date_posted.desc()).all() if current_user.register_as == 'hirer' else []
    saved_jobs = current_user.saved_jobs
    return render_template(
        "dashboard.html",
        title="Dashboard",
        profile_form=profile_form,
        job_form=job_form,
        skills=skills,
        posted_jobs=posted_jobs,
        js='dashboard',
        custom='dashboard',
        saved_jobs=saved_jobs
    )


@auth_pages.route("/save_job/<int:job_id>", methods=["POST"])
@login_required
def save_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    if job not in current_user.saved_jobs:
        current_user.saved_jobs.append(job)
        db.session.commit()
        flash("Job saved to your dashboard!", "success")
    else:
        flash("You have already saved this job.", "info")
    return redirect(url_for('main_pages.jobs'))

@auth_pages.route('/unsave_job/<int:job_id>', methods=['POST'])
@login_required
def unsave_job(job_id):
    try:
        # Find the job
        job = Jobs.query.get_or_404(job_id)
        
        # Check if the job is in current user's saved jobs
        if job in current_user.saved_jobs:
            # Remove the job from saved jobs
            current_user.saved_jobs.remove(job)
            db.session.commit()
            flash('Job removed from saved jobs', 'success')
        else:
            flash('Job was not in your saved jobs', 'warning')
        
        return redirect(url_for('auth_pages.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        auth_pages.logger.error(f"Error unsaving job: {e}")
        flash('An error occurred while removing the job', 'danger')
        return redirect(url_for('auth_pages.dashboard'))