# import time
# from datetime import datetime
from flask import Flask, render_template, g

from flask.ext.mail import Mail
from flask.ext.mongoset import MongoSet
from flask.ext.security import current_user

from .settings import CURRENT_SITE


def create_app(conf_module):
    app = Flask(__name__,
                static_url_path='/static/{}'.format(CURRENT_SITE),
                template_folder='static/{}'.format(CURRENT_SITE))
    app.config.from_object(conf_module)

    # Cache(app)
    Mail(app)
    MongoSet(app)
    # SQLAlchemy(app)

    with app.app_context():
        from city_lang.pages import bp as pages

        app.register_blueprint(pages)

        return app


def add_processing(app):

    @app.before_request
    def setup_session():
        g.user = current_user
        # g.now = time.mktime(datetime.utcnow().timetuple())

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('base.html'), 404

    return app


def init_app(conf_module='city_lang.settings'):
    return add_processing(create_app(conf_module))
