from flask.ext.wtf import Form, fields, validators


class RegistrationForm(Form):
    name = fields.TextField(u'First & Last name', [validators.Length(min=5)],
                description=u'John Doe')
    email = fields.TextField(u'Email', [validators.Email()],
                description=u'test@example.com')
    position = fields.TextField(u'Job Position', [validators.Length(min=5)],
                description=u'Senior Software Developer')
    company = fields.TextField(u'Company', [validators.Length(min=2)],
                description=u'Top 10 leader')
