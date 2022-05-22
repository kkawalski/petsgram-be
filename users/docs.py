from flask_restx import fields as api_fields

from app.docs import base_model
from users import users_ns


base_user = users_ns.clone("User", base_model, {
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
})

list_users = api_fields.List(api_fields.Nested(base_user))

register_user = users_ns.clone("RegisterUser", base_user, {
    "password": api_fields.String(
        description="User password",
        required=True,
    ),
    "password_submit": api_fields.String(
        description="User password submit",
        required=True,
    ),
})

login_req = users_ns.model("LoginRequest", {
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

login_res = users_ns.model("LoginResponse", {
    "access_token": api_fields.String(
        description="Access Token",
        readonly=True,
    ),
    "refresh_token": api_fields.String(
        description="Refresh Token",
        readonly=True,
    ),
})
