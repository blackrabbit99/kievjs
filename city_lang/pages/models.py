# encoding: utf-8
import trafaret as t

from city_lang.core.documents import Document
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
        'created_at': t.Type(datetime),
        t.Key('is_confirmed', default=True): t.Bool,
        t.Key('is_upproved', default=False): t.Bool,
        t.Key('is_declined', default=False): t.Bool,
    })

    def save_registered(self):
        if self.query.find_one({'email': self.email}) is None:
            self.created_at = datetime.utcnow()
            return self.save()
        else:
            return None


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
class Sponsor(Document):
    structure = t.Dict({
        'name': t.String,
        'description': t.String(allow_blank=True),
        'logo': t.Any,
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
