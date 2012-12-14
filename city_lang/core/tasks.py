from flask import current_app
from flask.ext.mail import Message

from werkzeug.local import LocalProxy


celery = LocalProxy(lambda: current_app.extensions['celery'])
mail = LocalProxy(lambda: current_app.extensions['mail'])


@celery.task
def send_email(rcpt, template, context):
    msg = Message("Hello", recipients=["nimnull@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
