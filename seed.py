# -*- encoding: utf-8 -*-
from datetime import datetime

from flask import current_app
from flask.ext.script import Command
from flask.ext.security.utils import encrypt_password

from werkzeug.local import LocalProxy

__all__ = ['Seed']

mongo = LocalProxy(lambda: current_app.extensions['mongoset'])
_security = LocalProxy(lambda: current_app.extensions['security'])

user_data = {
    'email': 'test@example.com',
    'password': 'test',
    'first_name': 'Somebody',
    'last_name': "Someone"
}


class Seed(Command):

    def create_user(self, user_data=user_data):
        user_data['password'] = encrypt_password(user_data['password'])
        user = _security.datastore.create_user(**user_data)
        _security.datastore.commit()
        return user

    def create_admin_user(self):
        current_app.config['ADMINS'] += (user_data['email'], )
        return _security.datastore.create_user(**user_data)

    def create_roles(self):
        for name in current_app.config['ROLES']:
            if _security.datastore.find_role(name) is None:
                _security.datastore.create_role(name=name)

    def run(self):
        # self.create_roles()
        # self.create_user()
        self.create_admin_user()
