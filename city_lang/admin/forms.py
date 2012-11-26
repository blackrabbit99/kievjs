from flask.ext.wtf import Form, fields, validators


class SpeakerForm(Form):
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Speaker's name")
    speech = fields.TextField(u'Speech title', [validators.Required()],
                description=u"Title for the speech")
    intro = fields.TextAreaField(u'Speech intro', [validators.Required()],
                description=u"A few words to introduce speech")


class SponsorForm(Form):
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Company title")
    description = fields.TextField(u'Description',
                description=u"A few words to describe (optional)")
    logo = fields.FileField(u'Logo')
