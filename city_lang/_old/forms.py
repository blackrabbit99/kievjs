from wtforms import Form, TextField, TextAreaField, \
    PasswordField, validators


__all__ = ("AuthForm", "UserForm")


class AuthForm(Form):
    username = TextField('Username', [validators.Length(min=2, max=25)])
    password = PasswordField('New Password', [validators.Required()])


class UserForm(Form):
    name = TextField('Username', [validators.Length(min=2, max=25)])
    email = TextField('Email', [validators.Email()])
    position = TextField('Position')
    company = TextField('Company')
    comments = TextAreaField('Comments')
