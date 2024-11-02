import logging
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

from config import Config

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.basicConfig(level= logging.INFO, format = f'%(asctime)s - %(levelname)s : %(message)s')
    db.init_app(app)

    #Import routes
    from app.views import views
    from app.auth import auth
    from app.employee import employee

    #Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(employee, url_prefix='/')

    from app.models.user import User

    with app.app_context():
        if not path.exists('app/' + DB_NAME):
            db.create_all()
            logging.info('Database created')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

