from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app import db
from app.employee.forms import EmployeeForm
from app.models.employee import Employee

views = Blueprint('views', __name__)

@views.route('/dashboard')
@login_required
def dashboard():
    form = EmployeeForm()
    returned_data = db.session.query(Employee).all()
    return render_template('grid.html', user=current_user, form=form, list=returned_data)
