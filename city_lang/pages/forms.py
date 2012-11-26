from wtforms import form, fields, validators


class SpeakerForm(form.Form):
    name = fields.TextField(u'Name', [validators.Required()],
                description=u"Speaker's name")
    speech = fields.TextField(u'Speech title', [validators.Required()],
                description=u"Title for the speech")
    intro = fields.TextAreaField(u'Speech intro', [validators.Required()],
                description=u"A few words to introduce speech")


class RegistrationForm(form.Form):
    name = fields.TextField(u'First & Last name', [validators.Length(min=5)],
                description=u'John Doe')
    email = fields.TextField(u'Email', [validators.Email()],
                description=u'test@example.com')
    position = fields.TextField(u'Job Position', [validators.Length(min=5)],
                description=u'Senior Software Developer')
    company = fields.TextField(u'Company', [validators.Length(min=5)],
                description=u'Top 10 leader')


