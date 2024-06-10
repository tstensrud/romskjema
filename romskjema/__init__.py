from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import logging


db = SQLAlchemy()
DB_NAME = "projects.db"
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "9UE5CwQRIJqM5O2SbDifX"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)

    logging.basicConfig(
        filename='log.log',
        level=logging.DEBUG,
        format = '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists('romskjema/' + DB_NAME):
        with app.app_context():
            db.create_all()

    