# -*- encoding: utf-8 -*-
from bson import ObjectId
from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required

from city_lang.core import http
from city_lang.core.utils import jsonify_status_code
from city_lang.pages.forms import SpeakerForm
from city_lang.pages.models import Speaker, User

from . import bp


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/speakers/', methods=['GET', 'POST'])
@login_required
def speakers():
    form = SpeakerForm(request.form or None)

    if request.form and form.validate():
        speaker = Speaker()
        form.populate_obj(speaker)
        speaker.save()
        return redirect(url_for('.speakers'))

    context = {
        'speakers': Speaker.query.all(),
        'form': form
    }
    return render_template('admin/speakers.html', **context)


@bp.route('/speakers/<id>', methods=['DELETE'])
@login_required
def remove_speaker(id):
    Speaker.query.remove({'_id': ObjectId(id)})
    return jsonify_status_code({}, http.NO_CONTENT)


@bp.route('/users/')
@login_required
def users():
    context = {
        'users': User.query.all(),
    }
    return render_template('admin/users.html', **context)
