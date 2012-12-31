# -*- encoding: utf-8 -*-
"""
    flask.ext.security.datastore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains an user datastore classes.

    :copyright: (c) 2012 by Yehor Nazarkin.
    :license: MIT, see LICENSE for more details.
"""
from flask.ext.security.datastore import Datastore, UserDatastore
from flask.ext.security.utils import encrypt_password

from flask.ext.social.datastore import ConnectionDatastore

from bson import ObjectId


class MongoSetDatastore(Datastore):
    def put(self, model):
        if "_id" not in model:
            model.save(model)
        else:
            model.update(model)
        return model

    def delete(self, model):
        model.delete()


class MongoSetUserDatastore(MongoSetDatastore, UserDatastore):
    """A MongoSet datastore implementation for Flask-Security that
    assumes the use of the Flask-MongoSet extension.
    """
    def __init__(self, db, user_model, role_model):
        MongoSetDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def create_user(self, **kwargs):
        """Creates and returns a new user from the given parameters."""
        kwargs['password'] = encrypt_password(kwargs.pop('password'))
        user = self.user_model(**self._prepare_create_user_args(**kwargs))

        return self.put(user)

    def find_user(self, **kwargs):
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs.pop('id'))
        return self.user_model.query.find_one(kwargs)

    def find_role(self, role):
        return self.role_model.query.find_one({'name': role})


class MongoSetConnectionDatastore(MongoSetDatastore, ConnectionDatastore):
    """A MongoSet datastore implementation for Flask-Social."""

    def __init__(self, db, connection_model):
        MongoSetDatastore.__init__(self, db)
        ConnectionDatastore.__init__(self, connection_model)

    def _query(self, **kwargs):
        return self.connection_model.query

    def find_connection(self, **kwargs):
        return self._query.find_one(**kwargs)

    def find_connections(self, **kwargs):
        return self._query.find(**kwargs)
