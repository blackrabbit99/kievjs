from flask import current_app, render_template
from flask.ext.mail import Message

from werkzeug.local import LocalProxy


# celery = LocalProxy(lambda: current_app.extensions['celery'])
mail = LocalProxy(lambda: current_app.extensions['mail'])


# @celery.task
def send_email(rcpt, template, context):
    msg = Message("Welcome to Kharkiv JS Conference!",
                  recipients=[rcpt])
    msg.body = render_template("{}.txt".format(template), **context)
    msg.html = render_template(template, **context)
    mail.send(msg)
