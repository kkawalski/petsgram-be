from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, current_user
from flask_restx import Resource

from app import jwt
from app.docs import error_model
from app.permissions import admin_only, with_profile_only
from users import auth_ns, profiles_ns
from users.docs import base_user, register_user, list_users, login_req, login_res, base_profile, list_profiles, my_profile
from users.models import User, Profile
from users.schemas import UserSchema, LoginSchema, ProfileSchema


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(is_active=True, id=identity).first()


@auth_ns.route("/login")
class LoginView(Resource):

    @auth_ns.expect(login_req)
    @auth_ns.response(200, "Success", login_res)
    @auth_ns.response(400, "Error", error_model)
    def post(self):
        schema = LoginSchema()
        user = schema.load(auth_ns.payload)
        res_data = {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user)
        }
        return schema.dump(res_data), 200


@auth_ns.route("/refresh")
class RefreshTokenView(Resource):

    @auth_ns.expect(login_req)
    @auth_ns.response(200, "Success", login_res)
    @auth_ns.response(401, "Unauthorized", error_model)
    @jwt_required(refresh=True)
    def post(self):
        res_data = {
            "access_token": create_access_token(current_user),
        }
        return res_data, 200


@auth_ns.route("/")
class UsersListCreateView(Resource):

    @auth_ns.response(200, "Success", list_users)
    @auth_ns.response(401, "Unauthorized", error_model)
    @auth_ns.response(403, "Forbidden", error_model)
    @auth_ns.doc(security="Bearer")
    @jwt_required()
    @admin_only
    def get(self):
        schema = UserSchema(many=True)
        return schema.dump(User.query.all()), 200

    @auth_ns.expect(register_user)
    @auth_ns.response(201, "Created", base_user)
    @auth_ns.response(400, "Error", error_model)
    def post(self):
        schema = UserSchema()
        user_data = schema.load(auth_ns.payload)
        user = User(**user_data).save()
        return schema.dump(user), 201


@auth_ns.route("/me")
class MeView(Resource):

    @auth_ns.response(200, "Success", base_user)
    @auth_ns.response(401, "Unauthorized", error_model)
    @auth_ns.doc(security="Bearer")
    @jwt_required()
    def get(self):
        schema = UserSchema()
        return schema.dump(current_user), 200


@profiles_ns.route("/")
class ProfileListCreateView(Resource):

    @profiles_ns.response(200, "Success", list_profiles)
    @profiles_ns.response(401, "Unauthorized", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def get(self):
        schema = ProfileSchema(many=True)
        query = Profile.query
        if not current_user.is_admin:
            query = query.filter(Profile.user.has(is_active=True))
        return schema.dump(query.all()), 200

    @profiles_ns.expect(base_profile)
    @profiles_ns.response(201, "Created", base_profile)
    @profiles_ns.response(400, "Error", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    def post(self):
        schema = ProfileSchema()
        profile_data = schema.load(profiles_ns.payload)
        profile = Profile(**profile_data).save()
        return schema.dump(profile), 201


@profiles_ns.route("/<int:profile_id>")
class ProfileRetrieveView(Resource):

    @profiles_ns.response(200, "Success", base_profile)
    @profiles_ns.response(401, "Unauthorized", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def get(self, profile_id):
        query = Profile.query
        if not current_user.is_admin:
            query = query.filter(Profile.user.has(is_active=True))
    
        profile = Profile.get_or_404(
            profile_id,
            query=query,
        )

        schema = ProfileSchema(exclude=("user",))
        return schema.dump(profile), 200


@profiles_ns.route("/my-profile")
class MyProfileView(Resource):

    @profiles_ns.response(200, "Success", my_profile)
    @profiles_ns.response(401, "Unauthorized", error_model)
    @profiles_ns.response(403, "Forbidden", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def get(self):
        schema = ProfileSchema()
        return schema.dump(current_user.profile), 200

    @profiles_ns.expect(base_profile)
    @profiles_ns.response(202, "Updated", my_profile)
    @profiles_ns.response(401, "Unauthorized", error_model)
    @profiles_ns.response(403, "Forbidden", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def put(self):
        schema = ProfileSchema()
        profile_data = schema.load(profiles_ns.payload, partial=True)
        profiles = Profile.query.filter_by(user_id=current_user.id)
        profiles.update(profile_data)
        profile = profiles.first().save()
        return schema.dump(profile), 202

    @profiles_ns.response(204, "No content")
    @profiles_ns.response(401, "Unauthorized", error_model)
    @profiles_ns.response(403, "Forbidden", error_model)
    @profiles_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def delete(self):
        current_user.is_active = False
        current_user.save()
        return {}, 204
