from flask_login import login_user, current_user
import pytest
from app import create_app, db
from app.models import Post, User
from tests import TestConfig
from app.auth.forms import LoginForm, RegistrationForm, LoginAuthentication, ResetPasswordForm, ResetPasswordRequestForm
from app.models import User
from flask import url_for
from werkzeug.urls import url_parse
from unittest.mock import patch
# creates app contexts and then removes it later
@pytest.fixture(scope="module")
def app_contexts():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield app, app_context
    db.session.remove()
    db.drop_all()
    app_context.pop()

# Returns a registered user and the credentials to login (user, username, password)
@pytest.fixture(scope="module")
def registeredUser():
    user = User(username="David", email="abc@example.com")
    user.set_password("test")
    db.session.add(user)
    db.session.commit()
    return user, "David", "test"

# Created fixture for the client
@pytest.fixture()
def client(app):
    return app.test_client()

# Fixture for authenticated users
def authenticated_user(client, app):
    with app.app_context():
        user = User(username='test', email='test@gmail.com')
        user.set_password('123456789')
        db.session.add(user)
        db.session.commit()

        client.post('/login', data=dict(username='tester1', password='123456789', remember_me=False), follow_redirects=True)
        yield user
        db.sesion.delete(user)
        db.session.commit()

def runner(app):
    return app.test_cli_runner()
def test_enable_2fa(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

def test_disable_2fa(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        
# Test login function
def test_login(client, auth):
    response = client.get('/login')
    assert b'Sign In' in response.data

    # Invalid login attempt
    response = auth.login()
    assert b'Invalid username or password' in response.data

    # Valid login attempt
    user = User.query.filter_by(username='test_user').first()
    password = 'test_password'
    user.set_password(password)
    db.session.commit()

    response = auth.login('test_user', password)
    assert response.headers['Location'] == url_for('main.index')

    # Test user being redirected to the originally requested page after logging in
    response = client.get('/private')
    assert response.headers['Location'] == url_for('auth.login')

    response = auth.login('test_user', password)
    assert response.headers['Location'] == url_for('main.private')


# Test reset_password_request function
def test_reset_password_request(client, app):
    response = client.get('/reset_password_request')
    assert b'Reset Password' in response.data

    # Invalid email address
    response = client.post('/reset_password_request', data=dict(
        email='invalid_email'
    ), follow_redirects=True)
    assert b'Check your email for the instructions to reset your password' not in response.data

    # Valid email address
    user = User.query.filter_by(username='test_user').first()

    with patch('app.auth.views.send_password_reset_email') as mock_send_email:
        response = client.post('/reset_password_request', data=dict(
            email=user.email
        ), follow_redirects=True)

        assert mock_send_email.called_once_with(user)

    assert b'Check your email for the instructions to reset your password' in response.data

    # Test reset_password function
    token = user.get_reset_password_token()
    response = client.get(f'/reset_password/{token}')
    assert b'Reset Password' in response.data

    # Invalid password
    response = client.post(f'/reset_password/{token}', data=dict(
        password='new_password',
        password2='wrong_password'
    ), follow_redirects=True)
    assert b'Your password has been reset.' not in response.data

    # Valid password
    response = client.post(f'/reset_password/{token}', data=dict(
        password='new_password',
        password2='new_password'
    ), follow_redirects=True)
    assert b'Your password has been reset.' in response.data

# Test for manage_authentication
def test_manage_authentication(client, auth):
    auth.login()
    response = client.post

    # Test logout function
def test_logout(client, auth):
    auth.login()

    response = auth.logout()
    assert response.headers['Location'] == url_for('main.index')
