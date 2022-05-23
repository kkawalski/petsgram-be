from flask_uploads import IMAGES
from marshmallow import fields as ma_fields, post_load, pre_load, validates, validates_schema, INCLUDE
from marshmallow.exceptions import ValidationError
from werkzeug.datastructures import FileStorage

from app import ma
from images.models import Image


class ImageSchema(ma.SQLAlchemyAutoSchema):
    object_id = ma_fields.Integer(dump_only=True)
    object_type = ma_fields.String(dump_only=True)
    object = ma_fields.Raw(load_only=True, required=True)

    file = ma_fields.Raw(load_only=True, required=True)
    url = ma_fields.Url(dump_only=True)
    filename = ma_fields.String(dump_only=True)

    class Meta:
        model = Image
        unknown = INCLUDE

    @validates("file")
    def validate_file(self, value):
        if not isinstance(value, FileStorage):
            raise ValidationError("Wrong file")
        if value.filename.split(".")[-1] not in IMAGES:
            raise ValidationError("Only images allowed")

    @validates("object")
    def validate_model(self, value):
        from users.models import Profile
        if not isinstance(value, (Profile, )):
            raise ValidationError("Image allowed only for profile and post")

