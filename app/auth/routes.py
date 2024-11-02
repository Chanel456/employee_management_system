import logging
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user import User
from app.auth import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        # need to add more validations here ????? check logic again
        if user:
            if check_password_hash(user.password, password):
               login_user(user, remember = True)
               logging.info('%s logged in successfully', user.first_name)
               flash('Logged in successfully.', category='success')

               return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category = 'error')
        else:
            flash('There is no account linked with this email address. Please create an account', category = 'error')

    return render_template('auth/login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logging.info('User: %s successfully logged out', current_user.first_name)
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # This logic should be moved else where
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('userType')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('An account already exists with this email address', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif user_type is None:
            flash('Please select a user type', category='error')
        else:
            is_admin = True if user_type == 'admin' else False
            try:
                new_user = User(email=email, first_name=first_name,
                                password=generate_password_hash(password1, method='scrypt'), is_admin=is_admin)
                db.session.add(new_user)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to register user: %s, {err}', first_name)
                flash('Unable to register user', category='error')
            else:
                logging.info('%s account created successfully', new_user.first_name)
                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html', user = current_user)