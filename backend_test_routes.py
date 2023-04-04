from flask_login import login_user, current_user
import pytest
from app import create_app, db
from app.models import Post, User
from tests import TestConfig
import random, string, requests

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

# Creating fixture to mock a post for the test user
@pytest.fixture(scope="module")
def post(registeredUser):
    user, username, password = registeredUser
    post = Post(body="test post", author=user)
    db.session.add(post)
    db.session.commit()
    return post


def test_login_api(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login-api", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

def test_enable_disable_2fa_api(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser

    with app.test_client() as client:
        # Log in the user
        data = {"username": username, "password": password}
        response = client.post("/auth/login-api", json=data)
        assert response.status_code == 200
        assert "session" in response.json
        session_cookie = response.json["session"]

        # Set session cookie for the client
        client.set_cookie("localhost", "session", session_cookie)

        # Get the current 2FA status
        initial_2fa_status = user.authentication

        # Toggle 2FA status
        headers, form_data = {"Content-Type": "application/json"}, {"authentication": "no" if initial_2fa_status else "yes"}
        response = client.post("/auth/manage_authentication_api", headers=headers, json=form_data)
        assert response.status_code == 200

        # Check if the 2FA status has been toggled
        db.session.refresh(user)
        assert user.authentication != initial_2fa_status

        # Toggle 2FA status back to the original state
        form_data["authentication"] = "yes" if initial_2fa_status else "no"
        response = client.post("/auth/manage_authentication_api", headers=headers, json=form_data)
        assert response.status_code == 200

        # Check if the 2FA status has been toggled back to the original state
        db.session.refresh(user)
        assert user.authentication == initial_2fa_status

def test_likes_and_dislikes_api(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser

    with app.test_client() as client:
        # Log in the user
        data = {"username": username, "password": password}
        response = client.post("/auth/login-api", json=data)
        assert response.status_code == 200
        assert "session" in response.json
        session_cookie = response.json["session"]

        # Set session cookie for the client
        client.set_cookie("localhost", "session", session_cookie)

        # when I am logged in and have created a post
        # and I dislike the post
        post.dislike_by(current_user)
        # It should increase the dislikes by 1 (from 0 to 1)
        assert post.dislikes == 1
        # then if I undislike it
        post.undislike_by(current_user)
        # It should decrease the dislikes by 1 (from 1 to 0)
        assert post.dislikes == 0

def test_create_post_api(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser

    with app.test_client() as client:
        # Log in the user
        data = {"username": username, "password": password}
        response = client.post("/auth/login-api", json=data)
        assert response.status_code == 200
        assert "session" in response.json
        session_cookie = response.json["session"]

        # Set session cookie for the client
        client.set_cookie("localhost", "session", session_cookie)

        # Create a new post
        headers, form_data = {"Content-Type": "application/json"}, {"post": "Test post from pytest"}
        response = client.post("/index-api", headers=headers, json=form_data)
        assert response.status_code == 200
        assert "message" in response.json
        assert response.json["message"] == "Post created successfully"

        # Check if the post was actually created in the database
        post = Post.query.filter_by(author=user, body=form_data["post"]).first()
        assert post is not None

def test_archive_api(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser

    with app.test_client() as client:
        # Log in the user
        data = {"username": username, "password": password}
        response = client.post("/auth/login-api", json=data)
        assert response.status_code == 200
        assert "session" in response.json
        session_cookie = response.json["session"]

        # Set session cookie for the client
        client.set_cookie("localhost", "session", session_cookie)

        # Make the user like the post
        post.like_by(user)
        db.session.commit()

        # Get the archived posts
        response = client.get("/archive-api")
        assert response.status_code == 200

        # Check if the response contains the liked post
        post_data = response.json
        assert len(post_data) == 1
        assert post_data[0]["id"] == post.id
        assert post_data[0]["body"] == post.body
        assert post_data[0]["author"] == user.username

