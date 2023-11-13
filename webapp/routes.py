from webapp.models import User,Skills
from flask import render_template ,url_for,flash ,redirect,request
from webapp.forms import RegistrationForm , LoginForm,AddForm,DeleteForm,UpdateForm
from webapp import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required




skills =[('Html',80),('Css',75),('Python',95),('My SQL',95)]
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",text='Measure Your Skill and Donte It !', title = "home",custom='home' )


@app.route("/about")
def about():
    return render_template("about.html",title="About",custom='about')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data,lname=form.lname.data,username=form.username.data,email=form.email.data,password=hash_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password , form.password.data)):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    skills=Skills.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html',title='Dashboard',skills=skills,custom='dashboard')

@app.route("/skills")
@login_required
def skills():
    with app.app_context():
        skills=Skills.query.filter_by(user_id=current_user.id)
    

    return render_template('skills.html',pagetitle='Skillspage',page_head='My Skills',description='This Skills Page',skills = skills,custom = 'skills',js="main2")

@app.route("/delete",methods=['GET','POST'])
def delete():
    form= DeleteForm()
    
    skills=Skills.query.filter_by(user_id=current_user.id)
    skills2=Skills.query.filter_by(user_id=current_user.id).all()
    if len(skills2)!=0:
        if form.validate_on_submit():
            skill_d = request.form.get('my-skills')
        
            with app.app_context():
                    skill=Skills.query.filter_by(user_id=current_user.id,title=skill_d).first()
                    db.session.delete(skill)
                    db.session.commit()
            flash(f"Skill deleted successfully for {skill.title}", "success")
            return redirect(url_for("skills"))
    else:
        flash(f"You Should to have skill to delete", category='error')
        return redirect(url_for("skills"))
    
    return render_template('delete.html',custom='delete',skills=skills ,form=form)

@app.route("/update",methods=['GET','POST'])
def update():
    form= UpdateForm()
    
    skills=Skills.query.filter_by(user_id=current_user.id)
    skills2=Skills.query.filter_by(user_id=current_user.id).all()
    if len(skills2)!=0:
        if form.validate_on_submit():
            skill_u = request.form.get('my-skills')
            progress =  form.skillProg.data
        
            with app.app_context():
                    skill=Skills.query.filter_by(user_id=current_user.id,title=skill_u).first()
                    skill.prog = progress
                    db.session.commit()
            flash(f" Progress of Skill  updated successfully for {skill_u}", "success")
            return redirect(url_for("skills"))
    else:
        flash(f"You Should to have skill to delete", category='error')
        return redirect(url_for("skills"))
    
    return render_template('update.html',custom='update',skills=skills ,form=form)




@app.route("/add",methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        skill = Skills(title=form.title.data, user_id=current_user.id, prog=form.skillProg.data, desc=form.desc.data)
        with app.app_context():
            db.session.add(skill)
            db.session.commit()
        flash(f"Skill added successfully for {form.title.data}", "success")
        return redirect(url_for("skills"))
    return render_template('add.html',custom='add',form=form)


# @app.route("/register",methods=['GET','POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(fname=form.fname.data,lname=form.lname.data,username=form.username.data,email=form.email.data,password=hash_password)
#         with app.app_context():
#             db.session.add(user)
#             db.session.commit()
#         flash(f"Account created successfully for {form.username.data}", "success")
#         return redirect(url_for("login"))
#     return render_template("register.html", title="Register", form=form)