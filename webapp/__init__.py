from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '3235T90IKEGARJOPAKFFWJAVSOZDMKrgrest5234tfbhu8iklo09iuytr' 
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///pythonic.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"



from webapp import routes