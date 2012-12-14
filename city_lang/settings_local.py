DEBUG = False
USE_X_SENDFILE = False

MONGODB_DATABASE = 'kharkivjs'
DEFAULT_MAIL_SENDER = '<info@kharkivjs.com>'

CURRENT_SITE = 'kharkivjs'
CURRENT_SITE_NAME = 'JSKharkiv'

SQLALCHEMY_DATABASE_URI = "mysql://root@localhost:3360/kharkivjs"
BROKER_URL = 'mongodb://localhost:27017/celery'
CELERY_RESULT_BACKEND = 'mongodb'

MAIL_FAIL_SILENTLY = False
MAIL_SERVER = 'localhost'


