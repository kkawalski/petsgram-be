from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from app.docs import error_model
from app.permissions import with_profile_only
from images import images_ns
from images.docs import base_image, upload_image_parser
from images.models import Image
from images.schemas import ImageSchema


@images_ns.route("/avatar")
class AvatarView(Resource):

    @images_ns.response(200, "Success", base_image)
    @images_ns.response(401, "Unauthorized", error_model)
    @images_ns.response(403, "Forbidden", error_model)
    @images_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def get(self):
        avatar = current_user.profile.avatar
        if not avatar:
            raise NotFound
        schema = ImageSchema()
        return schema.dump(avatar), 200

    @images_ns.expect(upload_image_parser)
    @images_ns.response(201, "Created", base_image)
    @images_ns.response(400, "Error", error_model)
    @images_ns.doc(security="Bearer")
    @jwt_required()
    @with_profile_only
    def post(self):
        args = upload_image_parser.parse_args()
        uploaded_image = args['file']
        schema = ImageSchema()
        image_data = schema.load({
            "file": uploaded_image,
            "object": current_user.profile,
        })
        avatar = Image(**image_data).save()
        return schema.dump(avatar), 201
