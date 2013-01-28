# -*- encoding: utf-8 -*-
import getpass

from email.utils import parseaddr

from flask import current_app
from flask.ext.script import Command

from werkzeug.local import LocalProxy

__all__ = ['Seed']

mongo = LocalProxy(lambda: current_app.extensions['mongoset'])
_security = LocalProxy(lambda: current_app.extensions['security'])

user_data = {
    'email': 'klymyshyn@gmail.com',
    'password': '11111',
    'first_name': 'Max',
    'last_name': "K",
    # 'current_login_at': datetime.utcnow(),
    # 'current_login_ip': '127.0.0.1',
    # 'login_count': 0,
}


class Seed(Command):

    def create_user(self, data=user_data):
        user = _security.datastore.create_user(**data)
        _security.datastore.commit()
        return user

    def create_admin_user(self, user_data):
        current_app.config['ADMINS'] += (user_data['email'], )
        return _security.datastore.create_user(**user_data)

    def create_roles(self):
        for name in current_app.config['ROLES']:
            if _security.datastore.find_role(name) is None:
                _security.datastore.create_role(name=name)

    def run(self):
        # self.create_roles()
        # self.create_user()
        data = user_data
        name = raw_input("Enter First and Last name: ")

        first_name, last_name = name.split(" ", 1)

        _email = raw_input("Enter email: ")
        _name, email = parseaddr(_email)

        if not email:
            raise ValueError("Please, enter valid email")

        password = getpass.getpass("Enter password: ")
        password1 = getpass.getpass("Repeat password: ")
        if not password:
            raise ValueError("Please, enter non-empty password")

        if password != password1:
            raise ValueError("Password doesn't match")

        data.update(dict(
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name))

        self.create_admin_user(data).save()
        _security.datastore.commit()

        print "User `{}` have been added".format(email)
