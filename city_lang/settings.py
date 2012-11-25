# -- Flask-specific settings
DEBUG = False
SECRET_KEY = "<your secret key>"
USE_X_SENDFILE = True
CSRF_ENABLED = True

# MongoSet configuration ----------------
MONGODB_DATABASE = 'kharkivjs'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
# should we unroll DBRef links to objects
MONGODB_AUTOREF = True
MONGODB_AUTOINCREMENT = False
MONGODB_FALLBACK_LANG = 'en'

# Flask-Mail sender for default email sender
DEFAULT_EMAIL_FROM = '<info@kharkivjs.com>'
DEFAULT_MAIL_SENDER = DEFAULT_EMAIL_FROM
MAIL_FAIL_SILENTLY = True

# Flask-Security settings for default email sender
SECURITY_EMAIL_SENDER = DEFAULT_EMAIL_FROM
# either user should confirm email after registration or no
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True

SECURITY_CONFIRM_URL = '/account/activate/'
SECURITY_LOGOUT_URL = '/account/signout'
SECURITY_POST_LOGIN_VIEW = '/account/'
SECURITY_POST_CONFIRM_VIEW = '/account/'

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
# Users with email adresses listed here will be created as administrators
ADMINS = ('admin@example.com', )
# role name constants
USER_ROLE = 'user'
ADMIN_ROLE = 'admin'
ORGANIZER_ROLE = 'organizer'

ROLES = [USER_ROLE, ADMIN_ROLE, ORGANIZER_ROLE]


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
