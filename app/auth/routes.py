import logging
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.auth import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = find_user_by_email(form.email.data)
        if user:
            if form.validate_on_submit():
                   login_user(user, remember = True)
                   logging.info('%s logged in successfully', user.first_name)
                   flash('Logged in successfully.', category='success')
                   return redirect(url_for('views.home'))
        else:
            flash('There is no account linked with this email address. Please create an account', category='error')

    return render_template('auth/login.html', user=current_user, form = form)

@auth.route('/logout')
@login_required
def logout():
    logging.info('User: %s successfully logged out', current_user.first_name)
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = find_user_by_email(form.email.data)
        if user:
            return flash('This is the flash message', category='error')
        elif form.validate_on_submit():
            is_admin = True if form.account_type.data == 'admin' else False
            try:
                new_user = User(email=form.email.data, first_name=form.first_name.data, password=generate_password_hash(form.password.data, method='scrypt'), is_admin=is_admin)
                db.session.add(new_user)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to register user: %s, {err}', form.first_name.data)
                flash('Unable to register user', category='error')
            else:
                logging.info('%s account created successfully', form.first_name.data)
                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.login'))
    return render_template('auth/register.html', user=current_user, form=form)

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()