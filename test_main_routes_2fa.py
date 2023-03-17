from flask import url_for
from flask_login import login_user, current_user
import pytest
from app import create_app, db
from app.models import Post, User
from tests import TestConfig

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
    user = User(username="john", email="john@example.com")
    user.set_password("test")
    db.session.add(user)
    db.session.commit()
    return user, "john", "test"

@pytest.fixture(scope="module")
def registeredUser_2fa_enabled():
    user2 = User(username="Notjohn", email="Notjohn@example.com")
    user2.set_password("test?")
    db.session.add(user2)
    db.session.commit()
    user2.authentication = True
    db.session.commit()
    return user2, "Notjohn", "test?"

# Creating fixture to mock a post for the test user
@pytest.fixture(scope="module")
def post(registeredUser):
    user, username, password = registeredUser
    post = Post(body="test post", author=user)
    db.session.add(post)
    db.session.commit()
    return post



def test_login_No_2fa(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        assert current_user.is_authenticated == False
        assert login_user(user, remember=True) == True


def test_login_2fa(app_contexts, registeredUser_2fa_enabled, post):
    app, app_context = app_contexts
    user2, username, password = registeredUser_2fa_enabled
    with app.test_client() as client:
        response = client.post("/auth/login", data={"username": username, "password": password}, follow_redirects=True)
        assert response.status_code == 200
        assert user2.authentication == True

        # Submitting an incorrect verification code
        response = client.post("/auth/login_authentication", data={"verificationCode": "DnV$HE$y7PEzUnjZ"}, follow_redirects=True)
        assert response.status_code == 200

        # Checking if the correct text is present in the response, indicating that the authentication page is displayed
        assert "Home" in response.get_data(as_text=True)


def test_login_2fa_wrong_code(app_contexts, registeredUser_2fa_enabled, post):
    app, app_context = app_contexts
    user2, username, password = registeredUser_2fa_enabled
    with app.test_client() as client:
        response = client.post("/auth/login", data={"username": username, "password": password}, follow_redirects=True)
        assert response.status_code == 200
        assert user2.authentication == True

        # Submitting an incorrect verification code
        response = client.post("/auth/login_authentication", data={"verificationCode": "WrongCode"}, follow_redirects=True)
        assert response.status_code == 200

        # Checking if the correct text is present in the response, indicating that the authentication page is displayed
        assert "Verify" in response.get_data(as_text=True)

# testing that once the dabase value for 2 factor aultentication is set to true, the database value is set to true
def test_2fa_enabled(app_contexts, registeredUser_2fa_enabled, post):
    app, app_context = app_contexts
    user2, username, password = registeredUser_2fa_enabled
    with app.test_client() as client:
        response = client.post("/auth/login", data={"username": username, "password": password}, follow_redirects=True)
        assert response.status_code == 200
        assert user2.authentication == True
        
# testing that once the dabase value for 2 factor aultentication is set to false, the database value is set to false
def test_2fa_disabled(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        response = client.post("/auth/login", data={"username": username, "password": password}, follow_redirects=True)
        assert response.status_code == 200
        assert user.authentication == False
