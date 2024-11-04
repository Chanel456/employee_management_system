from flask import render_template, Blueprint, jsonify
from flask_login import login_required, current_user

from app import db
from app.employee.forms import EmployeeForm
from app.enums.location_options import LocationOptions
from app.models.employee import Employee

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/table')
@login_required
def table():
    form = EmployeeForm()
    returned_data = db.session.query(Employee).all()
    location_options = list(LocationOptions)
    return render_template('grid.html', user=current_user, list=returned_data, location_options=location_options, form=form)