# encoding: utf-8
import trafaret as t

from city_lang.core.datastore import MongoSetUserDatastore
from city_lang.core.models import Document

from flask import current_app
from flask.ext.security import Security, RoleMixin, UserMixin
from flask.ext.security.utils import encrypt_password

from . import mongo


@mongo.register
class FlatPage(Document):
    """ A flatpage representation model
    """
    structure = t.Dict({
        'title': t.String,
        'slug': t.String,
        'content': t.String,
        'template': t.String,
        'login_required': t.Bool
    })


@mongo.register
class Speaker(Document):
    structure = t.Dict({
        'name': t.String,
        'intro': t.String
    })


@mongo.register
class Role(Document):
    structure = t.Dict({'name': t.String})


@mongo.register
class User(Document):
    structure = t.Dict({
        'email': t.Email,
        'password': t.String,
        'first_name': t.String,
        'last_name': t.String,
        'active': t.Bool,
        'roles': t.List[t.Type(Role)]
    })

    def __init__(self, **kwargs):
        kwargs['password'] = encrypt_password(kwargs['password'])
        super(User, self).__init__(**kwargs)

user_datastore = MongoSetUserDatastore(mongo, User, Role)
security = Security(current_app, user_datastore)
