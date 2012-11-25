from wtforms import form, fields, validators


class SpeakerForm(form.Form):
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Speaker's name")
    speech = fields.TextField(u'Speech title', [validators.Required()],
                description=u"Title for the speech")
    intro = fields.TextAreaField(u'Speech intro', [validators.Required()],
                description=u"A few words to introduce speech")


class RegistrationForm(form.Form):
    name = fields.TextField(u'Your name', [validators.Length(min=5)])
    position = fields.TextField(u'Position', [validators.Length(min=5)])
    company = fields.TextField(u'Company', [validators.Length(min=5)])
    email = fields.TextField(u'', [validators.Email()])
