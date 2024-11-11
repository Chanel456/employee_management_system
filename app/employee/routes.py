from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app import db
from app.employee import employee
from app.employee.forms import EmployeeForm
from app.models.employee import Employee, find_employee_by_id, find_employee_by_email, create_employee, update_employee, delete_employee

@login_required
@employee.route('/create', methods=['GET', 'POST'])
def create():
    form = EmployeeForm()
    if request.method == 'POST':
        retrieved_employee = find_employee_by_email(form.email.data)

        if retrieved_employee:
            flash('An employee with this email address already exists within the system', category='error')
        elif form.validate_on_submit():
            create_employee(form.email.data, form.first_name.data, form.last_name.data, form.team_name.data, form.role.data, form.location.data, form.date_joined.data)

    return render_template('employees/add-employee.html', user=current_user, form=form)

@login_required
@employee.route('/update', methods=['POST', 'GET'])
def update():
    form = EmployeeForm()
    employee_id = request.args.get('employee_id')
    retrieved_employee = find_employee_by_id(employee_id)
    if request.method == 'POST' and form.validate_on_submit():
        updated_employee = form.data
        updated_employee.pop('csrf_token', None)
        if retrieved_employee:
            update_employee(employee_id, updated_employee)
            redirect(url_for('views.dashboard'))
        else:
            flash('Employee cannot be updated as they do not exist', category='error',)

    return render_template('employees/update-employee.html', user = current_user, employee = retrieved_employee, form = form)

@login_required
@employee.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET' and current_user.is_admin:
        employee_id = request.args.get('employee_id')
        delete_employee(employee_id)

    return redirect(url_for('views.dashboard'))

# see if i need these endpoints, i might remove.
@login_required
@employee.route('/fetch_all', methods=['GET'])
def fetch_all_employees():
    return jsonify(db.session.query(Employee).all())
