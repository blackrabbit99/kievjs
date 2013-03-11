#!/usr/bin/env python
from flask.ext.script import Manager
from city_lang.application import init_app
# from city_lang.commands import ImportVisitors
from seed import Seed
from confirm import Confirm


def main():
    app = init_app()
    manager = Manager(app)
    manager.add_command('seed', Seed())
    manager.add_command('confirm', Confirm())
    # manager.add_command('import', ImportVisitors())
    manager.run()
    return app


if __name__ == '__main__':
    main()
