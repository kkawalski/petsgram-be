import io

from app.errors import WRONG_IMAGE_EXTENSION, WRONG_IMAGE_FILE
from images.models import Image
from users.models import Profile
from tests.conftest import FILE_UPLOAD_DEST


def test_avatar_create(client, common_user_token, profile_user_token):
    res = client.post("/images/avatar", follow_redirects=True, headers={
        "Authorization": f"Bearer {common_user_token}"
    })

    assert res.status_code == 403
    assert "message" in res.json


    res = client.post("/images/avatar", follow_redirects=True, 
        headers={
            "Authorization": f"Bearer {profile_user_token}",
        },
        data={
            "file": (io.BytesIO(b"abcdef"), 'test.txt')
        },
        content_type='multipart/form-data'
    )

    assert res.status_code == 400
    assert "message" in res.json
    assert WRONG_IMAGE_EXTENSION in res.json["message"]

    res = client.post("/images/avatar", follow_redirects=True, 
        headers={
            "Authorization": f"Bearer {profile_user_token}",
        },
        data={
            "file": "test.txt"
        },
        content_type='multipart/form-data'
    )

    assert res.status_code == 400
    assert "message" in res.json
    assert WRONG_IMAGE_FILE in res.json["message"]

    res = client.post("/images/avatar", follow_redirects=True, 
        headers={
            "Authorization": f"Bearer {profile_user_token}",
        },
        data={
            "file": (io.BytesIO(b"abcdef"), 'test.jpg')
        },
        content_type='multipart/form-data'
    )

    assert res.status_code == 201
    assert "url" in res.json
    
    image = Image.query.first()
    profile = Profile.query.first()
    
    assert image.object == profile
    assert image.path.startswith(FILE_UPLOAD_DEST)


def test_avatar_retrieve(client, common_user_token, profile_user_token):
    res = client.get("/images/avatar", follow_redirects=True, headers={
        "Authorization": f"Bearer {common_user_token}"
    })

    assert res.status_code == 403
    assert "message" in res.json

    res = client.get("/images/avatar", follow_redirects=True, headers={
        "Authorization": f"Bearer {profile_user_token}"
    })

    assert res.status_code == 404
    assert "message" in res.json


