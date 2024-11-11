import logging
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import create_user, find_user_by_email
from app.auth import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        logging.info('Logging login form data')
        logging.info(form.data)
        user = find_user_by_email(form.email.data)
        if user:
            if form.validate_on_submit():
                   login_user(user, remember = True)
                   logging.info('%s logged in successfully', user.first_name)
                   flash('Logged in successfully.', category='success')
                   return redirect(url_for('views.dashboard'))
        else:
            flash('There is no account linked with this email address. Please create an account', category='error')

    return render_template('auth/login.html', user=current_user, form=form)

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
            create_user(form.email.data, form.first_name.data, form.password.data, is_admin)
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', user=current_user, form=form)