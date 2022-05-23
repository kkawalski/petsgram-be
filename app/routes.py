from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound

from app import api


@api.errorhandler(ValidationError)
def handle_validation_errors(e):
    messages = str(set(["\n".join(messages) for messages in e.messages.values()]))
    e.data = {"message": messages}
    return e.data, 400

@api.errorhandler(NotFound)
def handle_validation_errors(e):
    # replace the body with JSON
    e.data = {"message": e.description}
    return e.data, 404


@api.route("/api")
class IndexView(Resource):
    def get(self):
        return {"ping": "pong"}


