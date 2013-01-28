# import time
# from datetime import datetime
# from celery import Celery
from flask import Flask, g

from flask.ext.mail import Mail
from flask.ext.mongoset import MongoSet
# from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, configure_uploads, patch_request_class

from .settings import CURRENT_SITE  # , BROKER_URL, CELERY_RESULT_BACKEND

# celery = Celery('city_lang', backend='mongodb', broker=BROKER_URL)


def create_app(conf_module):
    app = Flask(__name__, static_url_path='/static',
                static_folder='../static/{}'.format(CURRENT_SITE),
                template_folder='../templates/{}'.format(CURRENT_SITE))
    app.config.from_object(conf_module)
    # Cache(app)

    Mail(app)
    MongoSet(app)
    # SQLAlchemy(app)
    # app.extensions['celery'] = celery
    images = UploadSet('image')
    configure_uploads(app, (images))
    patch_request_class(app)

    # setup local assets
    try:
        from city_lang.assets_local import setup_assets
        setup_assets(app)
    except ImportError, e:
        print "No module assets_local: {}".format(e)

    try:
        getattr(
            __import__("city_lang.assets_{}".format(CURRENT_SITE)),
            "assets_{}".format(CURRENT_SITE)).setup_assets(app)
    except Exception, e:
        print "Can't use local assets: {}".format(e)

    with app.app_context():
        from city_lang.admin import bp as admin
        from city_lang.pages import bp as pages

        app.register_blueprint(admin)
        app.register_blueprint(pages)

        return app


def add_processing(app):

    @app.before_request
    def setup_session():
        g.is_registerable = True
        g.site_title = app.config['CURRENT_SITE_NAME']
        # g.now = time.mktime(datetime.utcnow().timetuple())

    @app.errorhandler(404)
    def page_not_found(error):
        from city_lang.pages.views import flatpage
        return flatpage()

    return app


def init_app(conf_module='city_lang.settings'):
    return add_processing(create_app(conf_module))
