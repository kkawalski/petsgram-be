from flask_jwt_extended import current_user
from marshmallow import fields as ma_fields, post_load, pre_load, validates_schema, INCLUDE, validate
from marshmallow.exceptions import ValidationError

from app import ma
from app.errors import PASSWORD_DOES_NOT_MATCH, USER_WITH_EMAIL_EXIST, WORNG_LOGIN_CREDENTIALS
from users.models import Profile, User
from images.schemas import ImageSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    password = ma_fields.String(required=True, load_only=True)
    password_submit = ma_fields.String(required=True, load_only=True)
    email = ma_fields.Email(required=True)
    has_profile = ma_fields.Boolean(dump_only=True)

    class Meta:
        model = User
        unknown = INCLUDE

    @validates_schema
    def validate_email_exist(self, data, **kwargs):
        users_cnt = User.query.filter_by(email=data["email"]).count()
        if users_cnt > 0:
            raise ValidationError(USER_WITH_EMAIL_EXIST, "email")

    @validates_schema
    def validate_password_submit(self, data, **kwargs):
        if data["password"] != data["password_submit"]:
            raise ValidationError(PASSWORD_DOES_NOT_MATCH, "password")

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
            raise ValidationError(WORNG_LOGIN_CREDENTIALS)
        return user


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    user = ma_fields.Nested(UserSchema, dump_only=True)
    first_name = ma_fields.String(required=True)
    last_name = ma_fields.String(required=True)
    user_id = ma_fields.Integer(load_only=True, required=True)
    avatar = ma_fields.Nested(ImageSchema, dump_only=True)

    class Meta:
        model = Profile
        include_fk = True
        unknown = INCLUDE

    @pre_load
    def add_user_to_data(self, data, **kwargs):
        data["user_id"] = current_user.id
        return data
