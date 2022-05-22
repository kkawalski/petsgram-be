from sqlalchemy_utils import generic_relationship
import werkzeug.datastructures

from app import db
from app.models import BaseModel
from images import UploadSet, avatars, posts


class Image(BaseModel):
    def __init__(self, *args, file: werkzeug.datastructures.FileStorage = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file = file

    filename = db.Column(db.String(255), unique=True, nullable=False)

    object_type = db.Column(db.Unicode(255))
    object_id = db.Column(db.Integer)
    object = generic_relationship(object_type, object_id)

    @property
    def upload_set(self) -> UploadSet:
        from users.models import Profile
        if self.object.is_type(Profile):
            return avatars
        # if self.object.us_type(Post):
        #     return posts

    @property
    def url(self) -> str:
        return self.upload_set.url(self.filename)

    def save(self) -> "Image":
        if self.file is not None:
            self.filename = self.upload_set.save(self.file)
        return super().save()

    def __repr__(self) -> str:
        return f"<Image {self.url}>"
