# -*- encoding: utf-8 -*-
from flask import current_app, render_template, request, \
    g, redirect, session
from flask.ext.security import current_user

from city_lang.core import http

from . import bp
from .forms import RegistrationForm
from .models import FlatPage, Speaker, Visitor, Sponsor


@bp.route("/")
def speakers():
    context = {
        'speakers': Speaker.query.all()
    }
    return render_template('speakers.html', **context)


@bp.route("/partners/")
def partners():
    partners_set = []
    for kind, value in current_app.config['PARTNERS_KINDS']:
        if Sponsor.query.find({'kind': kind}).count() > 0:
            partners_set.append((value, Sponsor.query.find({'kind': kind})))

    return render_template('partners.html', kinds=partners_set)


@bp.route("/venue/")
def venue():
    return render_template('venue.html', **{})


@bp.route("/organizers/")
def organizers():
    return render_template('organizers.html', **{})


@bp.route("/confirm/<user_id>/<confirm_id>/")
def confirm(user_id, confirm_id):
    visitor = Visitor.query.get_or_404(user_id)

    for n, confirm in visitor.confirmations:
        if confirm["cid"] == confirm_id:
            confirm["confirmed"] = True
            visitor.save_confirmation(confirm, index=n)

            session["confirm_user_id"] = visitor.id

            break

    return redirect("/confirmed/")


@bp.route("/update/", methods=["POST"])
def update():
    try:
        user_id = session["confirm_user_id"]
    except KeyError:
        return redirect("/update-error/")

    visitor = Visitor.query.get_or_404(user_id)
    visitor["tshirt_size"] = request.form["tshirt_size"]
    visitor.save()

    return redirect("/updated/")


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
        'form': form,
        'letters': Visitor.query.all()
    }

    return render_template('registration.html', **context)


def flatpage():
    page = FlatPage.query.find_one({'slug': request.path.strip('/')})

    if page is None:
        return render_template('404.html'), http.NOT_FOUND

    #if page.login_required and current_user.is_anonymous():
    #    return render_template('404.html'), http.NOT_FOUND

    template = page.get('template', 'flatpage.html')

    return render_template(template, page=page)
