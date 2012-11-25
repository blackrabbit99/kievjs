from flask import Blueprint, current_app
from werkzeug.local import LocalProxy

bp = Blueprint('pages', __name__, url_prefix="")
mongo = LocalProxy(lambda: current_app.extensions['mongoset'])
_security = LocalProxy(lambda: current_app.extensions['security'])

import views
import models
