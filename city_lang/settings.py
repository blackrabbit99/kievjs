# -- Flask-specific settings
DEBUG = True
SECRET_KEY = "9798s7fdamd90saf8sodfjk4qjhg43jfgjq43gfqpw97f[as09duf"
USE_X_SENDFILE = False
CSRF_ENABLED = True
# SERVER_NAME = 'localhost'
# SESSION_COOKIE_SECURE = True
# MongoSet configuration ----------------
MONGODB_DATABASE = 'kharkivjs'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
# should we unroll DBRef links to objects
MONGODB_AUTOREF = True
MONGODB_AUTOINCREMENT = False
MONGODB_FALLBACK_LANG = 'en'

# Flask-Mail sender for default email sender
DEFAULT_MAIL_SENDER = '<info@kharkivjs.com>'
MAIL_FAIL_SILENTLY = True
# MAIL_SERVER : default 'localhost'
# MAIL_PORT : default 25
# MAIL_USE_TLS : default False
# MAIL_USE_SSL : default False
# MAIL_DEBUG : default app.debug
# MAIL_USERNAME : default None
# MAIL_PASSWORD : default Nonee
# DEFAULT_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default False


# Flask-Security settings for default email sender
SECURITY_EMAIL_SENDER = DEFAULT_MAIL_SENDER
# either user should confirm email after registration or no
SECURITY_RECOVERABLE = True
# SECURITY_TRACKABLE = True

SECURITY_LOGIN_URL = '/admin/login/'
SECURITY_LOGOUT_URL = '/admin/logout/'

SECURITY_POST_LOGIN_VIEW = '/admin/'

SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ')(*ENB%WOI3j3kf'

# Flask-Social related settings
SOCIAL_URL_PREFIX = '/social'

SOCIAL_CONNECT_ALLOW_VIEW = "/account/"
SOCIAL_CONNECT_DENY_VIEW = "/account/"

SOCIAL_TWITTER = {
    'consumer_key': '---------',
    'consumer_secret': '---------'
}
SOCIAL_FACEBOOK = {
    'consumer_key': '---------',
    'consumer_secret': '---------'
}


# Site specific settings
CURRENT_SITE = 'kharkivjs'
CURRENT_SITE_NAME = 'JSKharkiv'
# Users with email adresses listed here will be created as administrators
ADMINS = ('admin@example.com', )
# role name constants
USER_ROLE = 'user'
ADMIN_ROLE = 'admin'
ORGANIZER_ROLE = 'organizer'

ROLES = [USER_ROLE, ADMIN_ROLE, ORGANIZER_ROLE]

import os

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))

UPLOADS_DEFAULT_DEST = rel('../uploads')
UPLOADS_DEFAULT_URL = '/uploads/'

# settings_local autoimport
import sys
import importlib

try:
    ls = importlib.import_module('city_lang.settings_local')
    for attr in dir(ls):
        if '__' not in attr:
            setattr(sys.modules[__name__], attr, getattr(ls, attr))
except ImportError:
    print "settings_local undefined"
