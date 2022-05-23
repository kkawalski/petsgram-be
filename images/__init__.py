from flask_uploads import UploadSet, IMAGES, configure_uploads

from app import api, app


avatars = UploadSet("avatars", IMAGES)
pictures = UploadSet("pictures", IMAGES)
configure_uploads(app, (avatars, pictures, ))


images_ns = api.namespace("images", "Images", "/images")
