from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from dotenv import load_dotenv 
import os




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth_pages.login"
login_manager.login_message_category = "info"

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] =os.getenv("my_secrit_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///skills.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from .auth import auth_pages
    from .skills import skill_pages
    from .routes import main_pages
    from .admin import admin_page, MyAdminIndexView,MyModelView,UserModelView
    from .models import User,Skills
    from .hidden import errors

    admin1 = Admin(app, index_view=MyAdminIndexView())
    admin1.add_view(MyModelView(Skills,db.session))
    admin1.add_view(UserModelView(User,db.session))

    app.register_blueprint(admin_page)
    app.register_blueprint(skill_pages)
    app.register_blueprint(main_pages)
    app.register_blueprint(auth_pages)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app