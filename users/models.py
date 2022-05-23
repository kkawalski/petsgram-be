from sqlalchemy_utils.types import EmailType, PasswordType

from app import db
from app.models import BaseModel
from images.models import Image


class User(BaseModel):
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)

    is_active = db.Column(db.Boolean, server_default="true")
    is_admin = db.Column(db.Boolean, server_default="false")

    @property
    def has_profile(self):
        return bool(self.profile)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Profile(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    user = db.relationship("User", lazy=False, backref=db.backref("profile", uselist=False, lazy=True))

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    @property
    def avatar(self) -> Image:
        return Image.query.filter_by(object=self).first()

    def __repr__(self) -> str:
        return f"<Profile {self.first_name} {self.last_name}>"


