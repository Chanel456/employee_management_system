import datetime
import logging
from dataclasses import dataclass

from flask import flash
from sqlalchemy.exc import SQLAlchemyError

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
    date_joined: datetime.datetime = db.Column(db.Date)
    created: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now())

def find_employee_by_id(employee_id):
    try:
        retrieved_employee = Employee.query.get(employee_id)
        return retrieved_employee
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')

def find_employee_by_email(email):
    try:
        retrieved_employee = Employee.query.filter_by(email=email).first()
        return retrieved_employee
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')

def create_employee(email: str, first_name: str, last_name: str, team_name: str, role: str, location: str, date_joined: datetime):
    try:
        new_employee = Employee(email=email, first_name=first_name, last_name=last_name,
                                team_name=team_name, role=role, location=location, date_joined=date_joined)
        db.session.add(new_employee)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Unable to create employee: %s, {err}', first_name)
        flash('Unable to create employee', category='error')
    else:
        logging.info('Employee %s created successfully', first_name)
        flash('Employee added successfully', category='success')

def update_employee(employee_id, updated_employee):
    try:
        db.session.query(Employee).filter_by(employee_id=employee_id).update(updated_employee)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Unable to update employee: %s, {err}', updated_employee['email'])
        flash('Unable to update employee', category='error')
    else:
        logging.info('Employee: %s successfully updated', updated_employee['email'])
        flash('Employee successfully updated')

def delete_employee(employee_id):
    retrieved_employee = find_employee_by_id(employee_id)
    if retrieved_employee:
        try:
            db.session.delete(retrieved_employee)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('Unable to delete employee: %s {err}', retrieved_employee['email'])
            flash('Unable to delete employee', category='error')
        else:
            logging.info('Employee: %s deleted successfully', retrieved_employee.first_name)
            flash('Employee deleted successfully', category='success')
    else:
        flash('Employee cannot be deleted as they do not exist', category='error')