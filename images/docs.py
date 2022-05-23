from flask_restx import fields as api_fields
from werkzeug.datastructures import FileStorage

from app.docs import base_model
from images import images_ns


base_image = images_ns.clone("Image", base_model, {
    "filename": api_fields.String(
        description="Image filename",
        readonly=True
    ),
    "url": api_fields.Url(
        description="Image url",
        readonly=True,
    ),
})

upload_image_parser = images_ns.parser()
upload_image_parser.add_argument("file", type=FileStorage, location='files', required=True)
