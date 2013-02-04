DEBUG = False
USE_X_SENDFILE = False

MONGODB_DATABASE = 'lvivjs'
DEFAULT_MAIL_SENDER = '<info@lvivjs.org.ua>'

CURRENT_SITE = 'lvivjs'
CURRENT_SITE_NAME = 'LvivJS'

SQLALCHEMY_DATABASE_URI = "mysql://root@localhost:3360/kharkivjs"
BROKER_URL = 'mongodb://localhost:27017/celery'
CELERY_RESULT_BACKEND = 'mongodb'

MAIL_FAIL_SILENTLY = False
MAIL_SERVER = 'localhost'

ADMINS = ('klymyshyn@gmail.com', )
