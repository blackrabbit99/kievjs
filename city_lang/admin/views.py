# -*- encoding: utf-8 -*-
from flask.ext.security import login_required
from flask import render_template, g, request

from city_lang.pages.models import Speaker, User
from city_lang.pages.forms import SpeakerForm

from . import bp


@bp.route('/')
@login_required
def index():
    print request.url, request.path
    return render_template('admin/index.html')


@bp.route('/speakers/', methods=['GET', 'POST'])
@login_required
def speakers():
    form = SpeakerForm(request.form or None)

    if request.form and form.validate():
        pass

    context = {
        'speakers': Speaker.query.all(),
        'form': form
    }
    return render_template('admin/speakers.html', **context)


@bp.route('/users/')
@login_required
def users():
    context = {
        'users': User.query.all(),
    }
    return render_template('admin/users.html', **context)
