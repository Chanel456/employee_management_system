import logging

from flask import session
from flask_login import current_user
from sqlalchemy.testing.plugin.plugin_base import logging

from app.models.user import User


def test_registration(client, app):
    client.post('/register', data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test', 'password': '1234567', 'confirm_password': '1234567'})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == 'test@gmail.com'

def test_login(client, app):
    client.post('/register', data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test', 'password': '1234567', 'confirm_password': '1234567'})
    response = client.post('/login', data={'email': 'test@gmail.com', 'password': '1234567'}, follow_redirects=True)

    with client:
        client.get('/')
        assert session['user_id'] == 1
    # assert current_user.email == ''
        # assert current_user.email == 'test@gmail.com'

