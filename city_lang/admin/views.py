# -*- encoding: utf-8 -*-
from flask import render_template, g, request
from city_lang.pages.models import Speaker, User

from . import bp


@bp.route('/')
def index():
    print request.url, request.path
    return render_template('admin/index.html')


@bp.route('/speakers/')
def speakers():
    context = {
        'speakers': Speaker.query.all(),
    }
    return render_template('admin/speakers.html', **context)


@bp.route('/users/')
def users():
    context = {
        'users': User.query.all(),
    }
    return render_template('admin/users.html', **context)
