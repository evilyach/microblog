from flask import Flask
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = "login"
mail = Mail(app)
moment = Moment(app)
babel = Babel(app)

from app import routes, models, errors, log
