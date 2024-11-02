import datetime
from dataclasses import dataclass

from app import db

@dataclass
class Employee(db.Model):
    employee_id: int = db.Column(db.Integer, primary_key = True)
    email: str = db.Column(db.String(150), unique = True)
    first_name: str = db.Column(db.String(150))
    last_name: str = db.Column(db.String(150))
    team_name: str = db.Column(db.String(150))
    role:str = db.Column(db.String(150))
    location: str = db.Column(db.String(150))
    date_joined: datetime.datetime = db.Column(db.DateTime)
    created: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now())

