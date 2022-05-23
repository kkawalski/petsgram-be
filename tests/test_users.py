from app.errors import USER_WITH_EMAIL_EXIST, PASSWORD_DOES_NOT_MATCH
from users.models import User, Profile
from tests.conftest import PROFILE_USER_EMAIL


def test_users_list(client, common_user_token, admin_user_token):
    res = client.get("/auth", follow_redirects=True, headers={
        "Authorization": f"Bearer {common_user_token}"
    })

    assert res.status_code == 403
    assert "message" in res.json

    res = client.get("/auth", follow_redirects=True, headers={
        "Authorization": f"Bearer {admin_user_token}"
    })
    assert res.status_code == 200
    assert len(res.json) == 2


def test_users_create(client):
    res = client.post("/auth", follow_redirects=True, json={
        "email": "test@test.com",
        "password": "test",
        "password_submit": "test",
    })

    assert res.status_code == 201
    assert User.query.count() == 1
    
    user = User.query.first()

    assert str(user.password) != "test"

    res = client.post("/auth", follow_redirects=True, json={
        "email": "test@test.com",
        "password": "test",
        "password_submit": "not_test",
    })

    assert res.status_code == 400
    assert "message" in res.json
    assert PASSWORD_DOES_NOT_MATCH in res.json["message"]
    assert USER_WITH_EMAIL_EXIST in res.json["message"] 


def test_profile_create(client, common_user_token):
    res = client.post("/profiles", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {common_user_token}"
        },
        json={
            "first_name": "FN",
            "last_name": "LN",
            "description": "DESCRIPTION",
        }
    )

    assert res.status_code == 201
    assert Profile.query.count() == 1
    assert User.query.first().has_profile


def test_profile_list(client, common_user_token, profile_user_token):
    res = client.get("/profiles", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    
    assert res.status_code == 403
    assert "message" in res.json

    res = client.get("/profiles", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {profile_user_token}"
        }
    )
    
    assert res.status_code == 200
    assert len(res.json) == 1


def test_profile_retrieve(client, common_user_token, profile_user_token):
    res = client.get("/profiles/1", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    
    assert res.status_code == 403
    assert "message" in res.json

    res = client.get("/profiles/1", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {profile_user_token}"
        }
    )
    
    assert res.status_code == 200
    assert res.json["id"] == 1
    assert "user" not in res.json


def test_my_profile(client, common_user_token, profile_user_token):
    res = client.get("/profiles/my-profile", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {common_user_token}"
        }
    )
    
    assert res.status_code == 403
    assert "message" in res.json

    res = client.get("/profiles/my-profile", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {profile_user_token}"
        }
    )
    
    assert res.status_code == 200
    assert "user" in res.json
    assert res.json["user"]["email"] == PROFILE_USER_EMAIL

    NEW_FIRST_NAME = "NEW_FIRST_NAME"
    res = client.put("/profiles/my-profile", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {profile_user_token}"
        },
        json = {
            "first_name": NEW_FIRST_NAME,
        }
    )
    
    assert res.status_code == 202
    assert Profile.query.first().first_name == NEW_FIRST_NAME

    res = client.delete("/profiles/my-profile", follow_redirects=True,
        headers = {
            "Authorization": f"Bearer {profile_user_token}"
        }
    )
    
    assert res.status_code == 204
    
    profile = Profile.query.first()

    assert profile is not None
    assert not profile.user.is_active


