# -*- encoding: utf-8 -*-

from flask import current_app
from flask.ext.script import Command

from werkzeug.local import LocalProxy

__all__ = ['Confirm']

mongo = LocalProxy(lambda: current_app.extensions['mongoset'])


class Confirm(Command):
    def run(self):
        print "Send confirmation email"
        return
        '''
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
        '''
