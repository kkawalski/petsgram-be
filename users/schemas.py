from marshmallow import fields as ma_fields,post_load, validates_schema 
from marshmallow.exceptions import ValidationError

from app import ma
from users.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    password = ma_fields.String(required=True, load_only=True)
    password_submit = ma_fields.String(required=True, load_only=True)
    email = ma_fields.Email(required=True)

    class Meta:
        model = User

    @validates_schema
    def validate_email_exist(self, data, **kwargs):
        users_cnt = User.query.filter_by(email=data["email"]).count()
        if users_cnt > 0:
            raise ValidationError("User with this email already exist", "email")

    @validates_schema
    def validate_password_submit(self, data, **kwargs):
        if data["password"] != data["password_submit"]:
            raise ValidationError("Passwords does not match", "password")

    @post_load
    def clean_password_submit(self, data, **kwargs):
        data.pop("password_submit", "")
        return data


class LoginSchema(ma.Schema):
    email = ma_fields.Email(load_only=True, required=True)
    password = ma_fields.String(load_only=True, required=True)
    access_token = ma_fields.String(dump_only=True)
    refresh_token = ma_fields.String(dump_only=True)

    class Meta:
        fields = (
            "email",
            "password",
            "access_token",
            "refresh_token",
        )

    @post_load
    def check_user(self, data, **kwargs):
        user = User.query.filter_by(email=data["email"]).first()
        if not user or user.password != data["password"]:
            raise ValidationError("Wrong email or password")
        return user
