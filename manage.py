#!/usr/bin/env python
from flask.ext.script import Manager
from city_lang.application import init_app
from seed import Seed


def main():
    app = init_app()
    manager = Manager(app)
    manager.add_command('seed', Seed())
    manager.run()
    return app


if __name__ == '__main__':
    main()
