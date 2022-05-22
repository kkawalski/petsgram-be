from flask_restx import Resource
from marshmallow.exceptions import ValidationError

from app import api

@api.errorhandler(ValidationError)
def handle_validation_errors(e):
    messages = str(set(["\n".join(messages) for messages in e.messages.values()]))
    e.data = {"message": messages}
    return e.data, 400


@api.route("/api")
class IndexView(Resource):
    def get(self):
        return {"ping": "pong"}


