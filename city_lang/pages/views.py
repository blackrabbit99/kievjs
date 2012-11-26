# -*- encoding: utf-8 -*-
from flask import render_template, request, g, redirect
from flask.ext.security import current_user

from city_lang.core import http

from . import bp
from .forms import RegistrationForm
from .models import FlatPage, Speaker, Visitor


@bp.route("/")
def speakers():
    context = {
        'speakers': Speaker.query.all()
    }
    return render_template('speakers.html', **context)


@bp.route("/partners/")
def partners():
    print 'partners'
    return render_template('partners.html', **{})


@bp.route("/venue/")
def venue():
    return render_template('venue.html', **{})


@bp.route("/organizers/")
def organizers():
    return render_template('organizers.html', **{})


@bp.route("/registration/", methods=['GET', 'POST'])
def registration():
    g.is_registerable = False
    form = RegistrationForm(request.form or None)

    if request.form and form.validate():
        visitor = Visitor()
        form.populate_obj(visitor)
        visitor.save_registered()
        return redirect('/thank-you/')

    context = {
        'form': form
    }
    return render_template('registration.html', **context)


def flatpage():
    path = request.path.strip('/')
    page = FlatPage.query.find_one({'slug': path})

    if page is None:
        return render_template('404.html'), http.NOT_FOUND

    if page.registration_required and current_user.is_anonymous():
        return render_template('404.html'), http.NOT_FOUND

    template = page.template_name or 'flatpage.html'

    return render_template(template, page=page)
