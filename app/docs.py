from flask_restx import fields as api_fields

from app import api

base_model = api.model("Base", {
    "id": api_fields.Integer(
        description="Id",
        readonly=True,
    ),
    "created": api_fields.DateTime(
        description="Created",
        readonly=True,
    ),
    "modified": api_fields.DateTime(
        description="Modified",
        readonly=True,
    ),
})

error_model = api.model("Error", {
    "message": api_fields.String(
        description="Error message"
    ),
})

