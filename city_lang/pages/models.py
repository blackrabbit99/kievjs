# encoding: utf-8
import uuid
import time

import trafaret as t

from city_lang.core.documents import EmbeddedDocument
from datetime import datetime
from flask.ext.security import RoleMixin, UserMixin

from ..core import tasks
from . import mongo
from city_lang.settings import DOMAIN


@mongo.register
class Event(EmbeddedDocument):
    structure = t.Dict({
        'name': t.String
    })


@mongo.register
class Visitor(EmbeddedDocument):
    confirm_fields = {
        "cid": t.String,
        "sent": t.Bool,
        "letter_id": t.String,
        "confirmed_at": t.Float,
        "confirmed": t.Bool}

    structure = t.Dict({
        'name': t.String,
        'email': t.Email,
        'position': t.String,
        'company': t.String,
        'created_at': t.Type(datetime),
        'confirms': t.List(t.Dict(confirm_fields)),
        'tshirt_size': t.String(allow_blank=False),
        t.Key('is_approved', default=False): t.Bool,
        t.Key('is_declined', default=False): t.Bool,
        t.Key('is_confirmed', default=False): t.Bool,
    })

    required_fields = ['name', 'email',
                       'is_approved', 'is_declined', 'confirms']

    def confirmations(self):
        if not hasattr(self, "confirms"):
            self.confirms = []

        return zip(
            range(1, len(self.confirms) + 1), self.confirms)
            #map(lambda o: {key: val for key, val in o.as_dict().items()
            #               if key != "id"}, self.confirms))

    @classmethod
    def confirmations_stats(cls):
        confirms = {}
        for visitor in cls.query.find({'confirms.confirmed': True}):
            for n, confirm in visitor.confirmations():
                if n not in confirms:
                    confirms[n] = 0

                if confirm["confirmed"] is True:
                    confirms[n] += 1
        return confirms

    @classmethod
    def tshirt_matrix(cls):
        return {}

    def one_confirm(self, letter_id):
        for n, confirm in self.confirmations():
            if confirm["letter_id"] == str(letter_id):
                return confirm

        return None

    def save(self, *args, **kwargs):
        self.save_confirmation(None, commit=True)

    def save_confirmation(self, confirm, index=None, commit=True):
        to_save = []

        for n, c in self.confirmations():
            if n == index:
                to_save.append(confirm)
            else:
                to_save.append(c)

        if index is None and confirm is not None:
            to_save.append(confirm)

        self.confirms = to_save

        if commit is True:
            super(Visitor, self).save()

    def send_confirmation(self, letter, id=None):
        if id is None:
            id = str(uuid.uuid1())

        for n, conf in self.confirmations():
            if "letter_id" in conf and \
                    conf["letter_id"] == str(letter.id):
                return False

        tasks.send_email(
            self.email,
            letter.subject,
            None, {
                'visitor': self,
                'id': id,
                'letter_id': letter.id,
                'link': "{}/confirm/{}/{}/".format(
                    DOMAIN, self.id, id)},
            template_text=letter.content)

        self.save_confirmation({
            "cid": id,
            "letter_id": str(letter.id),
            "sent": True,
            "confirmed": False,
            "confirmed_at": time.time()})

        return True

    def save_registered(self):
        if self.query.find_one({'email': self.email}) is None:
            self.created_at = datetime.utcnow()
            return self.save()
        else:
            return None


@mongo.register
class Letter(EmbeddedDocument):
    structure = t.Dict({
        "subject": t.String,
        "content": t.String,
        t.Key('content_html', default=None): t.String,
    })


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
