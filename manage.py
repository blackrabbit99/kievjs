#!/usr/bin/env python
from flask.ext.script import Manager
from city_lang.application import init_app


def main():
    app = init_app()
    manager = Manager(app)
    manager.run()
    return app


if __name__ == '__main__':
    main()
