from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types import URLType

from app import db


class BaseModel(db.Model):
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def save(self) -> "BaseModel":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> int:
        db.session.delete(self)
        db.session.commit()
        return self.id
