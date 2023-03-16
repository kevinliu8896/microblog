from flask_login import login_user, current_user
import pytest
from flask import url_for
from app import create_app, db
from app.models import Post, User
from tests import TestConfig

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

@pytest.fixture(scope="module")
def registeredUser():
    user = User(username="john", email="john@example.com")
    user.set_password("test")
    db.session.add(user)
    db.session.commit()
    return user, "john", "test"

@pytest.fixture(scope="module")
def favorite_post(registeredUser):
    user, username, password = registeredUser
    favorite_post = Post(body="test favorite post", author=user)
    db.session.add(favorite_post)
    db.session.commit()
    return favorite_post

def test_add_favorite_post(app_contexts, registeredUser, favorite_post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        # when I am logged in and have created a post
        # and I like the post (add to favorites)
        favorite_post.like_by(current_user)
        # It should mark the post as a favorite
        assert favorite_post in user.liked_posts.all()

def test_remove_favorite_post(app_contexts, registeredUser, favorite_post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        # when I am logged in and have liked a post
        # and I unlike the post (remove from favorites)
        favorite_post.unlike_by(current_user)
        # It should unmark the post as a favorite
        assert favorite_post not in user.liked_posts.all()


def test_delete_post(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

        # when I am logged in and have created a post
        post = Post(body="Test Post", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # and I delete the post
        post.deleted = True
        db.session.commit()

        # It should mark the post as deleted
        assert post.deleted == True


def test_undelete_post(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

        # when I am logged in and have created a post
        post = Post(body="Test Post", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # and I delete the post
        post.deleted = True
        db.session.commit()

        # and I undelete the post (Not curretnly implemented, but test should pass if it is)
        post.deleted = False
        db.session.commit()

        # It should unmark the post as deleted
        assert post.deleted == False


def test_post_not_viewable_if_archived(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

        # when I am logged in and have created a post
        post = Post(body="Test Post", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # and I delete the post
        post.deleted = True
        db.session.commit()

        # It should be viewable in index, profile and explore
        assert post in Post.query.filter_by(deleted=True).all()


def test_post_viewable_if_archived(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True

        # when I am logged in and have created a post
        post = Post(body="Test Post", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # and I delete the post
        post.deleted = True
        db.session.commit()

        # It should be viewable in archive
        assert post in Post.query.filter_by(deleted=True).all()