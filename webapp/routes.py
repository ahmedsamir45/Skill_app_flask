from webapp.models import Skills
from flask import render_template ,Blueprint


from flask_login import current_user,login_required


main_pages=Blueprint("main_pages",__name__)



@main_pages.route("/")
@main_pages.route("/home")
def home():
    return render_template("home.html",text='Measure Your Skill and Donte It !', title = "home",custom='home' )


@main_pages.route("/about")
def about():
    return render_template("about.html",title="About",custom='about')


@main_pages.route("/dashboard")
@login_required
def dashboard():
    skills=Skills.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html',title='Dashboard',skills=skills,custom='dashboard')
