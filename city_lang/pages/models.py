# encoding: utf-8
import trafaret as t

from city_lang.core.documents import Document, EmbeddedDocument
from datetime import datetime
from flask.ext.security import RoleMixin, UserMixin

from . import mongo


@mongo.register
class Event(EmbeddedDocument):
    structure = t.Dict({
        'name': t.String
    })


@mongo.register
class Visitor(EmbeddedDocument):
    structure = t.Dict({
        'name': t.String,
        'email': t.Email,
        'position': t.String,
        'company': t.String,
        'created_at': t.Type(datetime),
        t.Key('is_confirmed', default=False): t.Bool,
        t.Key('is_approved', default=False): t.Bool,
        t.Key('is_declined', default=False): t.Bool,
    })
    required_fields = ['name', 'email', 'is_confirmed',
                       'is_approved', 'is_declined']

    def save_registered(self):
        if self.query.find_one({'email': self.email}) is None:
            self.created_at = datetime.utcnow()
            return self.save()
        else:
            return None


@mongo.register
class FlatPage(EmbeddedDocument):
    """ A flatpage representation model
    """
    structure = t.Dict({
        'title': t.String,
        'slug': t.String,
        'content': t.String,
        'login_required': t.Bool,
        t.Key('template', default=''): t.String,
    })
    required_fields = ['title', 'slug', 'content']


@mongo.register
class Speaker(EmbeddedDocument):
    structure = t.Dict({
        'name': t.String,
        'speech': t.String,
        'intro': t.String
    })
    required_fields = ['name', 'speech']


@mongo.register
class Sponsor(EmbeddedDocument):
    structure = t.Dict({
        'name': t.String,
        'description': t.String(allow_blank=True),
        'url': t.String(allow_blank=True),
        'image': t.String(allow_blank=True),
        'kind': t.String
    })
    indexes = ['kind']

    required_fields = ['name']


@mongo.register
class Role(EmbeddedDocument, RoleMixin):
    structure = t.Dict({'name': t.String})


@mongo.register
class User(EmbeddedDocument, UserMixin):
    structure = t.Dict({
        'email': t.Email,
        'password': t.String,
        'first_name': t.String,
        'last_name': t.String,
        'roles': t.List[t.Type(Role)],
        t.Key('active', default=True): t.Bool,
    })
    required_fields = ['email', 'password', 'active']
