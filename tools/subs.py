# -*- coding: utf-8 -*-

import argparse
import base64
import getpass
import json
import os
import smtplib

from jinja2 import Template

from Crypto.Cipher import ARC4

import gdata.spreadsheet
import gdata.spreadsheets.client
import gdata.gauth


APP_ID = "KyivJS"
REGISTRATION_DOC_ID = "KyivJs Registration: November 17, 2012"

DEFAULT_EMAIL_PREFIX = "KyivJS Conference: "
EMAIL_DEFAULT_FROM = "klymyshyn@gmail.com"
EMAIL_DEFAULT_FROM_FULL = "KyivJS Team <klymyshyn@gmail.com>"

SCOPE = "https://spreadsheets.google.com/feeds/"
DB_FILE = ".kjsdb"
#REGISTRATION_DOC_ID = "KyivJs Registration: November 17, 2012"


ID = lambda o: o.id.text.rsplit("/", 1)[1]


class DB(object):
    """
    Deadly simple database
    """
    def __init__(self, token, path=DB_FILE):
        self.data = {}
        self.token = token[:8].zfill(8)
        arc = ARC4.new(self.token)

        if os.path.exists(DB_FILE):
            data = arc.decrypt(open(DB_FILE).read())
            self.data = json.loads(base64.b64decode(data))

    def update(self, key, value):
        # make sure object is serializable!
        json.dumps({key: value})

        self.data[key] = value

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]

        return None

    def save(self):
        arc = ARC4.new(self.token)

        data = base64.b64encode(json.dumps(self.data))

        fh = open(DB_FILE, "w")
        fh.write(arc.encrypt(data))
        fh.close()

        return True


def authenticate(args):
    """
    Authenticate application with oAuth2
    """
    db = DB(args.token)

    print "Authentication"

    # read oAuth credentials
    if db.oauth_client_id is None or db.oauth_client_secret is None:
        # read oAuth details
        client_id = raw_input("oAuth Client ID: ")
        client_secret = getpass.getpass("oAuth Secret: ")

        # save into database
        db.update("oauth_client_id", client_id)
        db.update("oauth_client_secret", client_secret)
        db.save()

    token = gdata.gauth.OAuth2Token(
        client_id=db.oauth_client_id,
        client_secret=db.oauth_client_secret,
        scope=SCOPE,
        user_agent=APP_ID
    )

    print token.generate_authorize_url()
    code = raw_input('Enter verification code: ').strip()

    # save into database
    db.update("oauth_access_token", token.get_access_token(code).access_token)
    db.update("oauth_refresh_token", token.refresh_token)
    db.save()

    print "You're successfully authenticated"


def get_auth(db):
    """
    Get authorized Spreadsheets client
    """
    print "Authentication..."
    if any([
        db.oauth_client_id is None,
        db.oauth_client_secret is None,
        db.oauth_access_token is None,
            db.oauth_refresh_token is None]):
        raise TypeError("Please, authorize with --auth command")

    token = gdata.gauth.OAuth2Token(
        client_id=db.oauth_client_id,
        client_secret=db.oauth_client_secret,
        scope=SCOPE,
        user_agent=APP_ID,
        access_token=db.oauth_access_token,
        refresh_token=db.oauth_refresh_token)

    client = gdata.spreadsheets.client.SpreadsheetsClient()
    token.authorize(client)

    return client


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


def get_worksheet(client, doc_id=None):
    try:
        sheet = [entry for entry in client.GetSpreadsheets().entry
                 if entry.title.text == doc_id][0]
    except IndexError, e:
        print "Can't find requested sheet, error: %r" % e
        return

    #tables = client.get_tables(ID(sheet))
    wsheet = client.GetWorksheets(ID(sheet))

    return sheet, wsheet


def get_users(client):
    """
    Get list of users
    """

    print "Get list of registered users..."
    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)

    users_map = {}
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))

    for num, row in enumerate(rows.entry):
        data = row.to_dict()
        if data.get("email") is None:
            print u"Warning: row #{0} not proper ({1})".format(num + 1, data)
            continue

        users_map[data.get("email").strip()] = data

    return users_map


def display_registrations(args):
    db = DB(args.token)
    client = get_auth(db)
    users_map = get_users(client)

    print "\nTotal registered users: {0}".format(len(users_map))


def send_mail(db, context, template=None):
    """
    Send HTML/Text mail using templates and GMail SMTP
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    html_template = u"{}.html".format(template)
    text_template = u"{}.txt".format(template)

    html_template = Template(open(html_template).read().decode("utf-8"))
    text_template = Template(open(text_template).read().decode("utf-8"))

    body_html = html_template.render(**context)
    body_text = text_template.render(**context)

    name, email = context["name"], context["email"]
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

    # msg["To"] = EMAIL_DEFAULT_FROM  ## testing only

    part1 = MIMEText(body_text.encode("utf-8"), "plain", "UTF-8")
    part2 = MIMEText(body_html.encode("utf-8"), "html", "UTF-8")

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
        smtp.sendmail(EMAIL_DEFAULT_FROM, email, msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        print "Can't send to {}".format(email)

    smtp.quit()


def send_registrations(args):
    db = DB(args.token)
    client = get_auth(db)
    users = get_users(client)

    total = len(users)
    sent = 1

    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))

    for num, row in enumerate(rows.entry):
        # TODO: parse timestamp
        info = row.to_dict()
        name = info["name"]
        email = info["email"]
        status = info["notification"]

        if email not in users:
            print u"User with email {} skipped "\
                  u"because of wrong format".format(email)
            continue

        if status:
            print u"Notification to {} already sent".format(name)
            sent += 1
            continue

        # timestamp = info["timestamp"]
        # company = info["company"]
        # position = info["position"]
        print u"Sending email to: {} ...".format(name)
        send_mail(db, info, template="templates/registration")

        # updating status
        info["notification"] = "sent"
        row.from_dict(info)
        client.update(row)

        print u"Sent {} of {}.".format(sent, total)
        sent += 1


parser = argparse.ArgumentParser(
    description="Manipulate subscription"
)

parser.add_argument(
    "--token", default=None, required=True,
    help="To encrypt/decrypt database we have to use "
    "some token. Should be at least 8 characters"
)
parser.add_argument(
    "--auth", action="store_true", default=False,
    help="Authenticate with Google and "
    "save token to {0} file".format(DB_FILE))

parser.add_argument(
    "--list", action="store_true", default=False,
    help="Show registrations")

parser.add_argument(
    "--send", action="store_true", default=False,
    help="Send registration confirmation")

args = parser.parse_args()


if args.auth:
    authenticate(args)
elif args.list:
    display_registrations(args)
elif args.send:
    send_registrations(args)
