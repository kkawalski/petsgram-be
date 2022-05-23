import os

from flask_uploads import configure_uploads

import pytest

from app import app, db
from images import avatars, pictures
from users.models import Profile, User


FILE_UPLOAD_DEST = "test_uploads"

PROFILE_USER_EMAIL = "profile@test.com"
PROFILE_USER_PASSWORD = "profile"
PROFILE_FIRST_NAME = "With"
PROFILE_LAST_NAME = "Profile"
PROFILE_DESCRIPTION = "With Profile"

COMMON_USER_EMAIL = "common@test.com"
COMMON_USER_PASSWORD = "common"

ADMIN_USER_EMAIL = "admin@test.com"
ADMIN_USER_PASSWORD = "admin"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["UPLOADS_DEFAULT_DEST"] = FILE_UPLOAD_DEST
    configure_uploads(app, (avatars, pictures, ))

    client = app.test_client()
    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()
        os.system("rm -rf test_uploads")


@pytest.fixture
def profile_user_token(client):
    user = User(email=PROFILE_USER_EMAIL, password=PROFILE_USER_PASSWORD).save()
    Profile(
        first_name=PROFILE_FIRST_NAME, 
        last_name=PROFILE_LAST_NAME,
        description=PROFILE_DESCRIPTION,
        user_id=user.id
    ).save()
    res = client.post("/auth/login", json={
        "email": PROFILE_USER_EMAIL,
        "password": PROFILE_USER_PASSWORD,
    })
    access_token = res.json.get("access_token")
    return access_token

@pytest.fixture
def common_user_token(client):
    User(email=COMMON_USER_EMAIL, password=COMMON_USER_PASSWORD).save()
    res = client.post("/auth/login", json={
        "email": COMMON_USER_EMAIL,
        "password": COMMON_USER_PASSWORD,
    })
    access_token = res.json.get("access_token")
    return access_token

@pytest.fixture
def admin_user_token(client):
    User(email=ADMIN_USER_EMAIL, password=ADMIN_USER_PASSWORD, is_admin=True).save()
    res = client.post("/auth/login", json={
        "email": ADMIN_USER_EMAIL,
        "password": ADMIN_USER_PASSWORD,
    })
    access_token = res.json.get("access_token")
    return access_token
