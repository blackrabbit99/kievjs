# import time
# from datetime import datetime
from flask import Flask, g

from flask.ext.mail import Mail
from flask.ext.mongoset import MongoSet

from .settings import CURRENT_SITE


def create_app(conf_module):
    app = Flask(__name__, static_url_path='/static',
                static_folder='../static/{}'.format(CURRENT_SITE),
                template_folder='../templates/{}'.format(CURRENT_SITE))
    app.config.from_object(conf_module)

    # Cache(app)

    Mail(app)
    MongoSet(app)

    # SQLAlchemy(app)

    with app.app_context():

        from city_lang.admin import bp as admin
        from city_lang.pages import bp as pages

        app.register_blueprint(admin)
        app.register_blueprint(pages)
        print app.url_map
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
