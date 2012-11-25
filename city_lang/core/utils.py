import re
from bson import ObjectId
# -*- encoding: utf-8 -*-
from datetime import datetime
from flask import json, current_app
from os.path import abspath, dirname, join


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.ctime()
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'as_dict'):
            return obj.as_dict()
        return super(CustomEncoder, self).default(obj)


def json_dumps(data):
    return json.dumps(data, indent=2, cls=CustomEncoder)


def jsonify_status_code(data=None, status=200):
    data = data or {}

    return current_app.response_class(json_dumps(data),
        status=status, mimetype='application/json')


def rules(language):
    """ helper method for getting plural form rules from the text file
    """
    rule_file = join(dirname(abspath(__file__)), 'rules.%s') % language
    for line in file(rule_file):
        pattern, search, replace = line.split()
        yield lambda word: re.search(pattern, word) and \
                re.sub(search, replace, word)


def plural_name(noun, language='en'):
    """ pluralize a noun for the selected language
    """
    for applyRule in rules(language):
        result = applyRule(noun)
        if result:
            return result


def underscorize(name):
    """ Converts CamelCase notation to the camel_case
    """
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


plural_underscored = lambda noun: plural_name(underscorize(noun))
