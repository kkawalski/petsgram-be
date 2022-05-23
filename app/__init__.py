from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

jwt = JWTManager(app)

ma = Marshmallow(app)

api = Api(app, authorizations={
    "Bearer": {
        "type": "apiKey", 
        "in": "header", 
        "name": "Authorization",
    },
})

from app import routes
from users import routes
from images import routes


