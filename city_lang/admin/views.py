# -*- encoding: utf-8 -*-
from bson import ObjectId
from flask import render_template, request, url_for, redirect
from flask.views import MethodView
from flask.ext.login import login_required

from city_lang.admin.forms import SpeakerForm, SponsorForm

from city_lang.core import http
from city_lang.core.utils import jsonify_status_code

from city_lang.pages.models import Speaker, Sponsor, User, Visitor

from . import bp


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/visitors/')
def visitors():
    context = {
        'visitors': Visitor.query.all()
    }
    return render_template('admin/registrations.html', **context)


@bp.route('/users/')
@login_required
def users():
    context = {
        'users': User.query.all(),
    }
    return render_template('admin/users.html', **context)


class CRUDView(MethodView):
    model = None
    form = None
    list_template = None
    item_form_template = 'admin/form_model.html'
    object_template = None

    decorators = [login_required]

    def get(self, id=None):
        if 'data' in request.args:
            instance = self.model.query.get_or_404(id)
            form = self.form(obj=instance)
            return jsonify_status_code({
                'form': render_template(self.item_form_template, form=form),
                'id': instance.id,
                'title': 'Editing {}'.format(self.__class__.__name__)
            })
        elif id is None:
            context = {'models': self.get_objects()}
            template = self.list_template
        else:
            context = {'model': self.model.query.get_or_404(ObjectId(id))}
            template = self.list_template

        context['form'] = self.form()
        return render_template(template, **context)

    def post(self):
        form = self.form(request.form)
        instance = self.model()

        if len(form.id.data) > 0:
            instance = self.model.query.get_or_404(form.id.data)

        if request.form and form.validate():
            form_data = form.data
            form_data.pop('id')

            instance.update(with_reload=False, **form_data)

            return redirect(url_for('.{}'.format(self.__class__.__name__)))

        context = {
            'models': self.get_objects(),
            'form': form
        }
        return render_template(self.list_template, **context)

    def delete(self, id):
        instance = self.model.query.get_or_404(ObjectId(id))
        instance.delete()
        return jsonify_status_code({}, http.NO_CONTENT)

    def get_objects(self, query_args=None):
        return self.model.query.find(query_args)


class SpeakerView(CRUDView):
    model = Speaker
    form = SpeakerForm
    list_template = 'admin/speakers.html'


class SponsorView(CRUDView):
    model = Sponsor
    form = SponsorForm
    list_template = 'admin/sponsors.html'
