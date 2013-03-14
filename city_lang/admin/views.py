# -*- encoding: utf-8 -*-
from bson import ObjectId

from flask import render_template, request, url_for, redirect
from flask.views import MethodView
from flask.ext.login import login_required
from flask.ext.uploads import UploadSet, UploadNotAllowed

from ..admin.forms import SpeakerForm, SponsorForm, PageForm, LetterForm
from ..core import http, tasks
from ..core.utils import jsonify_status_code
from ..pages.models import Speaker, Sponsor, User, Visitor, FlatPage, Letter
from .. import settings

from . import bp


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/visitors/')
@login_required
def visitors():
    context = {
        'letters': list(Letter.query.all()),
        'visitors': Visitor.query.all(),
        'approved': Visitor.query.find({'is_approved': True}).count(),
        'declined': Visitor.query.find({'is_declined': True}).count(),
        'confirmed': Visitor.confirmations_stats(),
        'tshirt_matrix': Visitor.tshirt_matrix()
    }
    return render_template('admin/registrations.html', **context)


@bp.route("/visitors/confirm/", methods=["GET"])
@login_required
def confirmation():
    letter = Letter.query.get(request.values["id"])

    for visitor in Visitor.query.all():
        visitor.send_confirmation(letter)

    return redirect("/admin/visitors/")


@bp.route('/manipulate/<id>', methods=['PUT'])
@login_required
def manipulate(id):
    visitor = Visitor.query.get_or_404(id)
    if 'action' in request.json:
        if request.json['action'] == 'approve':
            visitor.update(is_confirmed=True, is_approved=True,
                           is_declined=False, with_reload=False)
            tasks.send_email(visitor.email,
                             settings.APPROVE_PARTICIPIATION_SUBJECT,
                             'emails/approve.html',
                             {'visitor': visitor})
            response = {'response': 'approved'}
        elif request.json['action'] == 'decline':
            visitor.update(is_approved=False, is_declined=True,
                           with_reload=False)
            tasks.send_email(visitor.email,
                             settings.DECLINE_PARTICIPIATION_SUBJECT,
                             'emails/decline.html',
                             {'visitor': visitor})
            response = {'response': 'declined'}
        elif request.json['action'] == 'confirmation':
            letter = Letter.query.get(request.json['letter'])
            visitor.send_confirmation(letter)
            response = {"response": "confirmed"}
        else:
            response = {}
    return jsonify_status_code(response)


@bp.route('/state/<id>')
@login_required
def state(id):
    return render_template('admin/registrations_state.html',
                           visitor=Visitor.query.get_or_404(id))


@bp.route('/action/<id>')
@login_required
def action(id):
    return render_template('admin/registrations_action.html',
                           visitor=Visitor.query.get_or_404(id))


@bp.route('/users/')
@login_required
def users():
    context = {
        'users': User.query.all(),
        'letters': Letter.query.all()
    }
    return render_template('admin/users.html', **context)


class CRUDView(MethodView):
    model = None
    form = None
    list_template = None
    item_form_template = 'admin/form_model.html'
    object_template = None
    decorators = [login_required]
    upload_set = UploadSet('image')

    def extra_context(self, origin):
        return origin

    def get(self, id=None):
        if 'data' in request.args:
            instance = self.model.query.get_or_404(id)
            item_url = url_for('.{}'.format(self.__class__.__name__),
                               id=instance.id)
            form = self.form(obj=instance)
            return jsonify_status_code({
                'form': render_template(self.item_form_template, form=form,
                                        item_url=item_url),
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
        return render_template(
            template, **self.extra_context(context))

    def post(self, id=None):
        form = self.form(request.form)
        instance = self.model()

        if id is not None:
            instance = self.model.query.get_or_404(id)

        if request.form and form.validate():
            instance_data = form.data.copy()
            # processing uploaded files if any
            if 'image' in request.files:
                try:
                    filename = self.upload_set.save(request.files['image'])
                    instance_data['image'] = self.upload_set.url(filename)
                except UploadNotAllowed:
                    del instance_data['image']

            instance.update(upsert=True, **instance_data)

            return redirect(url_for('.{}'.format(self.__class__.__name__)))

        context = {
            'models': self.get_objects(),
            'form': form
        }
        return render_template(
            self.list_template, **self.extra_context(context))

    def delete(self, id):
        self.model.query.remove({'_id': ObjectId(id)})
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


class PageView(CRUDView):
    model = FlatPage
    form = PageForm
    list_template = 'admin/pages.html'


class LetterView(CRUDView):
    model = Letter
    form = LetterForm
    list_template = 'admin/letters.html'
