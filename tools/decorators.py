from functools import wraps

from flask import g, redirect, session

from db import mongo_init

__all__ = ("auth_only",)


# decorators
def auth_only(func):
    """
    Decorator to restrict access to the
    view only for authenticated users.

    Usage example:
        @app.route('/restricted-area/')
        @auth_only
        def resticted_view():
            ...
    """

    @wraps(func)
    def wrapper(*a, **kw):
        login = redirect('/api/login/')
        if not "username" in session:
            return login

        user = mongo_init().auth.find_one({
            "username": session["username"]})

        if not user:
            return login

        g.user = user

        return func(*a, **kw)
    return wrapper
