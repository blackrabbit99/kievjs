from flask import current_app, render_template
from flask.ext.mail import Message
from jinja2 import Template
from werkzeug.local import LocalProxy


celery = LocalProxy(lambda: current_app.extensions['celery'])
mail = LocalProxy(lambda: current_app.extensions['mail'])


@celery.task
def send_email(rcpt, subject, template, context,
               template_text=None,
               template_html=None):
    """
    Support to send emails with both files
    templates and plain text
    """
    msg = Message(subject,
                  recipients=[rcpt])

    render = lambda body, ctx: Template(body).render(**ctx)

    if template_text is not None:
        msg.body = render(template_text, context)
    elif template is not None:
        msg.body = render_template("{}.txt".format(template), **context)

    if template_html is not None:
        msg.html = render(template_html, context)
    elif template is not None:
        msg.html = render_template(template, **context)
    mail.send(msg)
