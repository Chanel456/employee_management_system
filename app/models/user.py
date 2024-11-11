from werkzeug.security import generate_password_hash

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean)

def create_user(email: str, first_name: str, password: str, is_admin: bool):
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='scrypt'), is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()
