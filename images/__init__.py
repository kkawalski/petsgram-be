from flask_uploads import UploadSet, IMAGES


avatars = UploadSet("avatars", IMAGES)
posts = UploadSet("posts", IMAGES)
