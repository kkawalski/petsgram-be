from flask_restx import Resource

from app import app, api


@api.route("/api")
class IndexView(Resource):
    def get(self, *args, **kwargs):
        return {"ping": "pong"}
