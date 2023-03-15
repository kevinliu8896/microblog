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
    user = User(username="David", email="abc@example.com")
    user.set_password("test")
    db.session.add(user)
    db.session.commit()
    return user, "David", "test"

def test_enable_2fa(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        client.post("/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.is_authenticated == True
