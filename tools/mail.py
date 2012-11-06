import getpass
import os
import smtplib
import settings

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

from jinja2 import Environment, FileSystemLoader

# getting configuration from settings
DEFAULT_EMAIL_PREFIX = getattr(settings, "DEFAULT_EMAIL_PREFIX", None)
EMAIL_DEFAULT_FROM = getattr(settings, "EMAIL_DEFAULT_FROM", None)
EMAIL_DEFAULT_FROM_FULL = getattr(settings, "EMAIL_DEFAULT_FROM_FULL", None)
DEBUG = getattr(settings, "DEBUG", False)


jinja_env = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), "templates"), "utf-8"))


__all__ = "smtp_connection_details", "send_mail"


def smtp_connection_details(db):
    """
    Get SMTP connection details
    """
    if db.smtp_host is None:
        db.update("smtp_host", raw_input("SMTP Host: "))

    if db.smtp_login is None:
        db.update("smtp_login", raw_input("Email login: "))

    if db.smtp_password is None:
        db.update("smtp_password", getpass.getpass("SMTP Password: "))

    db.save()

    return db.smtp_host, db.smtp_login, db.smtp_password


def send_mail(db, context, template=None, files=[]):
    """
    Send HTML/Text mail using templates and GMail SMTP
    """

    html_template = u"{}.html".format(template)
    text_template = u"{}.txt".format(template)

    html_template = jinja_env.get_template(html_template)
    text_template = jinja_env.get_template(text_template)

    body_html = html_template.render(**context)
    body_text = text_template.render(**context)

    name, email = context["name"].strip(), context["email"].strip()
    company, position = context["company"], context["position"]

    # preparing
    msg = MIMEMultipart("alternative")
    msg.set_charset("utf-8")

    msg["Subject"] = u"{} Registration Confirmation".format(
        DEFAULT_EMAIL_PREFIX)
    msg["From"] = EMAIL_DEFAULT_FROM_FULL
    try:
        msg["To"] = u"{} <{}>".format(
            name.encode("utf-8"), email.encode("utf-8"))
    except UnicodeDecodeError:
        msg["To"] = email

    if DEBUG:
        del msg["To"]
        msg["To"] = EMAIL_DEFAULT_FROM  # testing only

    part1 = MIMEText(body_text.encode("utf-8"), "plain", "UTF-8")
    part2 = MIMEText(body_html.encode("utf-8"), "html", "UTF-8")

    # attach files to the letter
    if files:
        for file in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file).read())
            Encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment; filename="{}"'.format(os.path.basename(file)))

            msg.attach(part)

    msg.attach(part1)
    msg.attach(part2)

    # sending via SMTP, working ONLY with Gmail
    host, login, pwd = smtp_connection_details(db)

    smtp = smtplib.SMTP(host, 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login, pwd)
    #
    try:
        smtp.sendmail(EMAIL_DEFAULT_FROM, [email], msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        print "Can't send to {}".format(email)

    smtp.quit()
