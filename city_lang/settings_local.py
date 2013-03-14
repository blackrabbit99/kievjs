DEBUG = False
USE_X_SENDFILE = False

MONGODB_DATABASE = 'lvivjs'
DEFAULT_MAIL_SENDER = '<info@lvivjs.org.ua>'

CURRENT_SITE = 'lvivjs'
CURRENT_SITE_NAME = 'LvivJS'

DOMAIN = "http://lvivjs.org.ua"  ## no trailing slash
SQLALCHEMY_DATABASE_URI = "mysql://root@localhost:3360/kharkivjs"
BROKER_URL = 'mongodb://localhost:27017/celery'
CELERY_RESULT_BACKEND = 'mongodb'

MAIL_FAIL_SILENTLY = False
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025

ADMINS = ('klymyshyn@gmail.com', )


APPROVE_PARTICIPIATION_SUBJECT = "Welcome to LvivJS Conference!"
DECLINE_PARTICIPIATION_SUBJECT = "Sorry, you can't participiate LvivJS"
