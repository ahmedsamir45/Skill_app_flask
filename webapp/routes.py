from webapp.models import Skills,User,Jobs
from flask import render_template ,Blueprint





main_pages=Blueprint("main_pages",__name__)

from flask import render_template
from webapp.models import User, Jobs
from webapp import db

main_pages = Blueprint("main_pages", __name__)

@main_pages.route("/")
@main_pages.route("/home")
def home():
    return render_template("home.html", text='Measure Your Skill and Donte It !', title="home", custom='home')

@main_pages.route("/about")
def about():
    return render_template("about.html", title="About", custom='about')

@main_pages.route("/people")
def people():
    search_query = request.args.get('search', '')  # Get search query from URL parameters
    
    if search_query:
        # Perform case-insensitive search on multiple fields
        people = User.query.filter(
            db.or_(
                User.username.ilike(f'%{search_query}%'),
                User.fname.ilike(f'%{search_query}%'),
                User.lname.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%'),
                User.bio.ilike(f'%{search_query}%'),
                User.skills.any(Skills.title.ilike(f'%{search_query}%'))
            )
        ).all()
    else:
        people = User.query.all()
    
    return render_template('people.html', title='people', custom='people', 
                         people=people, search_query=search_query,js="search")

@main_pages.route("/jobs")
def jobs():
    search_query = request.args.get('search', '')  # Get search query from URL parameters
    
    # Base query
    jobs_query = Jobs.query.order_by(Jobs.date_posted.desc())
    
    if search_query:
        # Perform case-insensitive search on multiple fields
        jobs_query = jobs_query.filter(
            db.or_(
                Jobs.title.ilike(f'%{search_query}%'),
                Jobs.company.ilike(f'%{search_query}%'),
                Jobs.description.ilike(f'%{search_query}%'),
                Jobs.skills_required.ilike(f'%{search_query}%'),
                Jobs.type.ilike(f'%{search_query}%'),
                Jobs.posted_by.has(User.username.ilike(f'%{search_query}%'))
            )
        )
    
    all_jobs = jobs_query.all()
    return render_template("jobs.html", jobs=all_jobs, user=current_user, 
                         custom="jobs", search_query=search_query,js="search")

@main_pages.route("/job/<int:job_id>")
def job_detail(job_id):
    job = Jobs.query.get_or_404(job_id)
    return render_template("job_detail.html", job=job)


from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from webapp.models import User, Skills, Jobs
from webapp import db

@main_pages.route('/user/<string:username>')
def user_info(username):
    try:
        # Get the user by username
        user = User.query.filter_by(username=username).first_or_404()
        
        # Get user's skills ordered by date posted
        skills = Skills.query.filter_by(author=user)\
                            .order_by(Skills.date_posted.desc())\
                            .all()
        
        # Get jobs posted by this user
        jobs_posted = Jobs.query.filter_by(posted_by=user)\
                               .order_by(Jobs.date_posted.desc())\
                               .all()
        
        return render_template('user_info.html', 
                             title=user.username,
                             user=user,
                             skills=skills,
                             jobs_posted=jobs_posted)
    
    except Exception as e:
        print(f"Error in user_info route: {str(e)}")
        abort(500)