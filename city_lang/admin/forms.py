from flask import current_app
from flask.ext.wtf import Form, fields, validators


class SpeakerForm(Form):
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Speaker's name")
    speech = fields.TextField(u'Speech title', [validators.Required()],
                description=u"Title for the speech")
    intro = fields.TextAreaField(u'Speech intro', [validators.Required()],
                description=u"A few words to introduce speech")


class SponsorForm(Form):
    kind = fields.SelectField(u'Kind',
                              choices=current_app.config['PARTNERS_KINDS'])
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Company title")
    description = fields.TextAreaField(u'Description',
                description=u"A few words to describe (optional)")
    url = fields.TextField(u'URL', description=u"Site URL")
    image = fields.FileField(u'Logo')


class PageForm(Form):
    title = fields.TextField(u'Title', [validators.Required()],
                             description=u'Page Title')
    slug = fields.TextField(u'Slug', [validators.Required()],
                            description=u'Page Slug')
    content = fields.TextAreaField(u'Content', [validators.Required()],
                                   description='Content text')
    login_required = fields.BooleanField(u'Requires login')
