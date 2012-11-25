from flask import abort
from flask.ext.security import current_user

from functools import wraps

from . import http


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated():
            abort(http.UNAUTHORIZED)
        return fn(*args, **kwargs)

    return wrapper


class ClassProperty(property):
    def __init__(self, method, *args, **kwargs):
        method = classmethod(method)
        return super(ClassProperty, self).__init__(method, *args, **kwargs)

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


classproperty = ClassProperty
