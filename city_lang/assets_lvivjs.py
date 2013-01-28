from flask.ext.assets import Environment, Bundle


def setup_assets(app):
    assets = Environment(app)
    assets.init_app(app)

    css = Bundle(
        "css/bootstrap.css",
        "css/layout.css",
        output="css/_style.css")

    js = Bundle(
        "js/jquery.min.js",
        "js/jquery.router.js",
        "js/custom.js",
        output="js/_basic.js")

    assets.register('css_all', css)
    assets.register('js_all', js)
