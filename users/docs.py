from flask_restx import fields as api_fields

from app.docs import base_model
from images.docs import base_image
from users import auth_ns, profiles_ns


base_user = auth_ns.clone("User", base_model, {
    "email": api_fields.String(
        description="User email",
        required=True, 
        example="example@email.com",
        pattern='\S+@\S+\.\S+',
    ),
    "is_active": api_fields.Boolean(
        description="Is user active",
        readonly=True,
    ),
    "is_admin": api_fields.Boolean(
        description="Is user admin",
        readonly=True,
    ),
    "has_profile": api_fields.Boolean(
        description="Is user has profile",
        readonly=True,
    ),
})

list_users = api_fields.List(api_fields.Nested(base_user))

register_user = auth_ns.clone("RegisterUser", base_user, {
    "password": api_fields.String(
        description="User password",
        required=True,
    ),
    "password_submit": api_fields.String(
        description="User password submit",
        required=True,
    ),
})

login_req = auth_ns.model("LoginRequest", {
    "email": api_fields.String(
        description="User email",
        required=True, 
        example="example@email.com",
        pattern='\S+@\S+\.\S+',
    ),
    "password": api_fields.String(
        description="User password",
        required=True,
    ),
})

login_res = auth_ns.model("LoginResponse", {
    "access_token": api_fields.String(
        description="Access Token",
        readonly=True,
    ),
    "refresh_token": api_fields.String(
        description="Refresh Token",
        readonly=True,
    ),
})

base_profile = profiles_ns.clone("Profile", base_model, {
    "first_name": api_fields.String(
        description="User email",
        required=True,
    ),
    "last_name": api_fields.String(
        description="Is user active",
        required=True,
    ),
    "description": api_fields.String(
        description="Is user admin",
    ),
    "avatar": api_fields.Nested(base_image)
})

list_profiles = api_fields.List(api_fields.Nested(base_profile))

# my_profile = profiles_ns.clone("MyProfile", base_profile, {
#     "user": api_fields.Nested(base_user),
# })
