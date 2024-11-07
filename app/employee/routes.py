import logging
from datetime import datetime

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.employee import employee
from app.employee.forms import EmployeeForm
from app.models.employee import Employee

@login_required
@employee.route('/create', methods=['GET', 'POST'])
def create():
    form = EmployeeForm()
    if request.method == 'POST':
        retrieved_employee = find_employee_by_email(form.email.data)

        if retrieved_employee:
            flash('An employee with this email address already exists within the system', category='error')
        elif form.validate_on_submit():
            date_joined= datetime.strptime(str(form.date_joined.data), '%Y-%m-%d')
            try:
                new_employee = Employee(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, team_name=form.team_name.data,
                                        role=form.role.data, location=form.location.data, date_joined=date_joined)
                db.session.add(new_employee)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create employee: %s, {err}', form.first_name.data)
                flash('Unable to update employee', category='error')
            else:
                logging.info('Employee %s created successfully', form.first_name.data)
                flash('Employee added successfully', category='success')

    return render_template('employees/add-employee.html', user=current_user, form=form)

@login_required
@employee.route('/update', methods=['POST', 'GET'])
def update():
    form = EmployeeForm()
    employee_id = request.args.get('employee_id')
    retrieved_employee = find_employee_by_id(employee_id)
    if request.method == 'POST':
        updated_employee = form.data
        updated_employee.pop('csrf_token', None)
        #write function for date time
        converted_date = datetime.strptime(str(form.date_joined.data), '%Y-%m-%d')
        updated_employee['date_joined'] = converted_date

        if retrieved_employee:
            try:
                db.session.query(Employee).filter_by(employee_id=employee_id).update(updated_employee)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to update employee: %s, {err}', retrieved_employee['email'])
                flash('Unable to update employee', category='error')
            else:
                logging.info('Employee: %s successfully updated', updated_employee['first_name'])
                flash('Employee successfully updated')
                redirect(url_for('views.dashboard'))
        else:
            flash('Employee cannot be updated as they do not exist', category='error',)
    return render_template('employees/update-employee.html', user = current_user, employee = retrieved_employee, form = form)



# need to add check for admin
@login_required
@employee.route('/delete', methods=['GET', 'POST'])
def delete():
    #Look to see how i can send a proper delete request
    # Fall back for method not allow
    if request.method == 'GET' and current_user.is_admin:
        employee_id = request.args.get('employee_id')
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

    return redirect(url_for('views.dashboard'))

def find_employee_by_email(email):
    try:
        retrieved_employee = Employee.query.filter_by(email=email).first()
        return retrieved_employee
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')

def find_employee_by_id(employee_id):
    try:
        retrieved_employee = Employee.query.get(employee_id)
        return retrieved_employee
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')


# see if i need these endpoints, i might remove.
@login_required
@employee.route('/fetch_all', methods=['GET'])
def fetch_all_employees():
    return jsonify(db.session.query(Employee).all())