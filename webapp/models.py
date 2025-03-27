from datetime import datetime
from webapp import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default="default/default.png")  # Increased length
    password = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    resume_link = db.Column(db.String(255), nullable=True)
    register_as = db.Column(db.String(255), nullable=True)
    skills = db.relationship("Skills", backref="author", lazy=True)
    # def get_auth_token(self):
    #     """
    #     Generates a secure token for 'remember me' functionality
    #     """
    #     data = [str(self.id), self.password]  # Password acts as salt
    #     return login_manager._token_serializer.dumps(data)
    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prog = db.Column(db.Integer, nullable=False)

    desc = db.Column(db.String(32), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def __repr__(self):
        return f"Lesson('{self.title}', '{self.date_posted}')"



class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    company_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(255), nullable=False)
    link_to_apply = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)

    # Relationship to the user who posted the job
    posted_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    posted_by = db.relationship("User", backref="posted_jobs")

    # Relationship to users who saved the job (many-to-many)
    saved_by = db.relationship("User", secondary="job_saves", backref="saved_jobs")

    def __repr__(self):
        return f"Job('{self.title}', '{self.company}', '{self.date_posted}')"


# Association table for many-to-many relationship between Jobs and Users (for saving jobs)
job_saves = db.Table(
    "job_saves",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("job_id", db.Integer, db.ForeignKey("jobs.id"), primary_key=True),
)