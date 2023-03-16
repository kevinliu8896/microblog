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

# Creating fixture to mock a post for the test user
@pytest.fixture(scope="module")
def post(registeredUser):
    user, username, password = registeredUser
    post = Post(body="test post", author=user)
    db.session.add(post)
    db.session.commit()
    return post

def test_likeby_unlikeby(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        # when I am logged in and have created a post
        # and I like the post
        post.like_by(current_user)
        # It should increase the likes by 1 (from 0 to 1)
        assert post.likes == 1
        # then if I unlike it
        post.unlike_by(current_user)
        # It should decrease the likes by 1 (from 1 to 0)
        assert post.likes == 0

# testing dislikeby and undislikeby
def test_dislikeby_undislikeby(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        # when I am logged in and have created a post
        # and I dislike the post
        post.dislike_by(current_user)
        # It should increase the dislikes by 1 (from 0 to 1)
        assert post.dislikes == 1
        # then if I undislike it
        post.undislike_by(current_user)
        # It should decrease the dislikes by 1 (from 1 to 0)
        assert post.dislikes == 0

# testing laughby and unlaughby
def test_laughby_unlaughby(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
        # when I am logged in and have created a post
        # and I laugh at the post
        post.laugh_by(current_user)
        # It should increase the laughs by 1 (from 0 to 1)
        assert post.laughs == 1
        # then if I unlaugh it
        post.unlaugh_by(current_user)
        # It should decrease the laughs by 1 (from 1 to 0)
        assert post.laughs == 0


