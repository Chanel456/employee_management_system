import logging
from flask import Flask, render_template, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from os import path

from werkzeug.utils import redirect

from config import Config

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app(config_class=Config):
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

@app.route('/')
def redirect_to_home():
   return redirect(url_for('views.dashboard'))

@app.errorhandler(404)
def handle_not_found_error(error):
    return render_template('error/404.html', user=current_user), 404