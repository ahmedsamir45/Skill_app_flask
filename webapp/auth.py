
from webapp.models import User
from flask import render_template ,url_for,flash ,redirect,request
from webapp.forms import RegistrationForm , LoginForm
from webapp import bcrypt,db
from flask_login import login_user,current_user,logout_user
from flask import Blueprint


auth_pages = Blueprint("auth_pages",__name__)

@auth_pages.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data,lname=form.lname.data,username=form.username.data,email=form.email.data,password=hash_password)
       
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("auth_pages.login"))
    return render_template("register.html", title="Register", form=form)

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
            return redirect(next_page) if next_page else redirect(url_for("main_pages.home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@auth_pages.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main_pages.home"))
