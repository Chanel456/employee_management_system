import logging
from datetime import datetime

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, SQLAlchemyError

from app import db
from app.employee import employee
from app.enums.location_options import LocationOptions
from app.models.employee import Employee

@login_required
@employee.route('/create', methods=['GET', 'POST'])
def create_employee():
    location_options = list(LocationOptions)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        team_name = request.form.get('teamName')
        role = request.form.get('role')
        location = request.form.get('location')
        # write function to format date_joined
        date_joined = datetime.strptime(request.form.get('dateJoined'), '%Y-%m-%d')
        retrieved_employee = Employee.query.filter_by(email=email).first()

        if retrieved_employee:
            flash('An employee with this email address already exists within the system', category='error')
        else:
            # add some validation about the inputs
            try:
                new_employee = Employee(email=email, first_name=first_name, last_name=last_name, team_name=team_name,
                                        role=role, location=location, date_joined=date_joined)
                db.session.add(new_employee)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create employee: %s, {err}', first_name)
                flash('Unable to update employee', category='error')
            else:
                logging.info('Employee %s created successfully', new_employee.first_name)
                flash('Employee added successfully', category='success')

    return render_template('employees/add-employee.html', user=current_user, location_options=location_options)

@login_required
@employee.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        employee_id = request.args.get('employee_id')
        updated_employee = request.form.to_dict()
        retrieved_employee = Employee.query.get(employee_id)
        # write function to format date joined
        converted_date = datetime.strptime(request.form.get('date_joined'), '%Y-%m-%d')
        updated_employee['date_joined'] = converted_date

        if retrieved_employee:
            # add some validation about the inputs
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
        else:
            flash('Employee cannot be updated as they do not exist', category='error')
        return redirect(url_for('views.table'))



# need to add check for admin
@login_required
@employee.route('/delete', methods=['GET'])
def delete():
    #Look to see how i can send a proper delete request
    # Fall back for method not allow
    if request.method == 'GET' and current_user.is_admin:
        employee_id = request.args.get('employee_id')
        retrieved_employee = Employee.query.get(employee_id)
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
            flash('Employee cannot be deleted as the do not exist', category='error')

    return redirect(url_for('views.table'))


# see if i need these endpoints, i might remove.
#if endpoints are kept add try catch block
@login_required
@employee.route('/fetch_all', methods=['GET'])
def fetch_all_employees():
    return jsonify(db.session.query(Employee).all())

@login_required
@employee.route('/fetch_employee', methods=['GET'])
def fetch_employee():
    employee_id = request.args.get('employee_id')
    if employee_id:
        return jsonify(Employee.query.get(employee_id))
    # need to add code for else. Incorrect query parameter received