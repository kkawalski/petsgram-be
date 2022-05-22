from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, current_user
from flask_restx import Resource

from app import jwt
from app.docs import error_model
from users import users_ns
from users.docs import base_user, register_user, list_users, login_req, login_res
from users.models import User
from users.schemas import UserSchema, LoginSchema


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@users_ns.route("/login")
class LoginView(Resource):
    @users_ns.expect(login_req)
    @users_ns.response(200, "Success", login_res)
    @users_ns.response(400, "Error", error_model)
    def post(self):
        schema = LoginSchema()
        user = schema.load(users_ns.payload)
        res_data = {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user)
        }
        return schema.dump(res_data), 200


@users_ns.route("/refresh")
class RefreshView(Resource):
    @users_ns.expect(login_req)
    @users_ns.response(200, "Success", login_res)
    @users_ns.response(401, "Unauthorized", error_model)
    @jwt_required(refresh=True)
    def post(self):
        res_data = {
            "access_token": create_access_token(current_user),
        }
        return res_data, 200


@users_ns.route("/")
class UsersListCreateView(Resource):
    @users_ns.response(200, "Success", list_users)
    @users_ns.response(401, "Unauthorized", error_model)
    @users_ns.doc(security="Bearer")
    @jwt_required()
    def get(self):
        schema = UserSchema(many=True)
        return schema.dump(User.query.all()), 200

    @users_ns.expect(register_user)
    @users_ns.response(201, "Success", base_user)
    @users_ns.response(400, "Error", error_model)
    def post(self):
        schema = UserSchema()
        user_data = schema.load(users_ns.payload)
        user = User(**user_data).save()
        return schema.dump(user), 201
