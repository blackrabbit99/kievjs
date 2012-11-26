# encoding: utf-8
import trafaret as t

from city_lang.core.models import Document
from datetime import datetime
from flask.ext.security import RoleMixin, UserMixin

from . import mongo


@mongo.register
class Event(Document):
    structure = t.Dict({
        'name': t.String
    })


@mongo.register
class Visitor(Document):
    structure = t.Dict({
        'name': t.String,
        'email': t.Email,
        'position': t.String,
        'company': t.String,
        t.Key('created_at', default=datetime.utcnow): t.Type(datetime),
    })


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
        'speech': t.String,
        'intro': t.String
    })


@mongo.register
class Role(Document, RoleMixin):
    structure = t.Dict({'name': t.String})


@mongo.register
class User(Document, UserMixin):
    structure = t.Dict({
        'email': t.Email,
        'password': t.String,
        'first_name': t.String,
        'last_name': t.String,
        'roles': t.List[t.Type(Role)],
        t.Key('active', default=True): t.Bool,
    })
