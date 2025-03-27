from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from dotenv import load_dotenv 
import os
from datetime import timedelta, datetime  # Added both imports

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth_pages.login"
login_manager.login_message_category = "info"
login_manager.remember_cookie_duration = timedelta(days=30) 

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_PERMANENT"] = True
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    app.config.update(
        REMEMBER_COOKIE_SECURE=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_DURATION=timedelta(days=30),
        SESSION_COOKIE_SAMESITE='Lax'
    )

    # User loader is required
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # Before request handler
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            db.session.refresh(current_user)  # Refresh user session
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    # Rest of your imports and registrations
    from .auth import auth_pages
    from .skills import skill_pages
    from .routes import main_pages
    from .admin import admin_page, MyAdminIndexView, MyModelView, UserModelView, SkillsModelView, JobsModelView
    from .models import User, Skills, Jobs
    from .hidden import errors

    admin1 = Admin(app, index_view=MyAdminIndexView())
    admin1.add_view(UserModelView(User, db.session, name='Users'))
    admin1.add_view(SkillsModelView(Skills, db.session, name='Skills'))
    admin1.add_view(JobsModelView(Jobs, db.session, name='Jobs'))

    app.register_blueprint(admin_page)
    app.register_blueprint(skill_pages)
    app.register_blueprint(main_pages)
    app.register_blueprint(auth_pages)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app
