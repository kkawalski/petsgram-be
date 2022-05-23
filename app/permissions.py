from functools import wraps

from flask_jwt_extended import current_user


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user is not None and current_user.is_admin:
            return func(*args, **kwargs)
        return {"message": "Less permissions for this action"}, 403
    return wrapper


def with_profile_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user is not None and current_user.has_profile:
            return func(*args, **kwargs)
        return {"message": "Need to create profile"}, 403
    return wrapper