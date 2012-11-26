from city_lang.core.datastore import MongoSetUserDatastore
from flask import Blueprint, current_app
from flask.ext.security import Security

from werkzeug.local import LocalProxy

bp = Blueprint('pages', __name__, url_prefix="")
mongo = LocalProxy(lambda: current_app.extensions['mongoset'])
_security = LocalProxy(lambda: current_app.extensions['security'])

import views
import models

user_datastore = MongoSetUserDatastore(mongo, models.User, models.Role)
Security(current_app, user_datastore)
