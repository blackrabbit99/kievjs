from flask.ext.assets import Environment, Bundle


def setup_assets(app):
    assets = Environment(app)
    assets.init_app(app)

    css = Bundle(
        "stylesheets/foundation.css",

        "stylesheets/foundation_icons_general/"
        "stylesheets/general_foundicons.css",

        "stylesheets/app.css",
        output="stylesheets/_basic_style.css")

    js = Bundle(
        "javascripts/jquery.js",
        "javascripts/modernizr.foundation.js",
        "javascripts/galleria.js",
        "javascripts/app.js",
        output="javascripts/_basic.js")

    assets.register('css_all', css)
    assets.register('js_all', js)
