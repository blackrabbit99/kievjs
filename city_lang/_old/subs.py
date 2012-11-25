# -*- coding: utf-8 -*-

import argparse
import getpass
import pymongo

import uuid

from codes import generate_code, generate_badge
from db import DB, DB_FILE, mongo_init
from mail import send_mail

import gdata.spreadsheet
import gdata.spreadsheets
import gdata.spreadsheets.client
import gdata.gauth

from api import REGID, generate_confirmation

import settings


# getting configuration from settings
APP_ID = getattr(settings, "APP_ID", None)
REGISTRATION_DOC_ID = getattr(settings, "REGISTRATION_DOC_ID", None)
CAMPAIGNS = getattr(settings, "CAMPAIGNS", {})
DEBUG = getattr(settings, "DEBUG", False)
CONFIRMATION_URL = getattr(settings, "CONFIRMATION_URL", "")
REGISTRATION_URL = getattr(settings, "REGISTRATION_URL", "")
BADGE_TITLE = getattr(settings, "BADGE_TITLE", "")
SCOPE = "https://spreadsheets.google.com/feeds/"


ID = lambda o: o.id.text.rsplit("/", 1)[1]


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


def send_registrations(args):
    db = DB(args.token)
    client = get_auth(db)
    users = get_users(client)

    total = len(users)
    sent = 1

    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))
    sent_mails = set()

    for num, row in enumerate(rows.entry):
        # TODO: parse timestamp
        info = row.to_dict()
        name = info["name"].strip()
        email = info["email"].strip()
        status = info["notification"]

        # avoid duplicates
        if email in sent_mails:
            print u"User with email: {} already notified".format(email)
            continue

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
        send_mail(db, info, template="registration")

        # updating status
        info["notification"] = "sent"
        row.from_dict(info)
        client.update(row)

        print u"Sent {} of {}.".format(sent, total)
        sent_mails.add(email)
        sent += 1


def send_confirmation(args):
    db = DB(args.token)

    if not args.campaign:
        raise ValueError(
            u"Please, provide --campaign argument value."
            u"Available campaigns: {}".format(", ".join(CAMPAIGNS.values())))

    confirmation_shake = args.campaign
    external_id = [key for key, val in CAMPAIGNS.iteritems()
                   if val == confirmation_shake][0]

    collection = mongo_init().users
    users = collection.find({}).sort("order", pymongo.ASCENDING)

    total = users.count()
    sent = 1
    sent_mails = set()

    for num, user in enumerate(users):
        name = user["name"].strip()
        email = user["email"].strip()
        status = user["notification"]
        user_id = user["internalid"]

        # avoid duplicates
        if email in sent_mails:
            print u"User with email: {} already notified".format(email)
            continue

        if status and status == confirmation_shake:
            print u"Confirmation request to {} already sent".format(email)
            sent_mails.add(email)
            sent += 1
            continue

        print u"Sending Confirmation `{}` to: {} ...".format(
            name, confirmation_shake)

        # prepare context
        link = CONFIRMATION_URL.format(external_id, user_id)
        badge = generate_confirmation(user_id)

        if badge is None:
            print u"Can't generate PDF for {}".format(user_id)
            continue

        context = dict([(key, val) for key, val in user.iteritems()])
        context["link"] = link

        # send mail
        send_mail(db, context, template="confirmation", files=[badge])

        # updating status
        user["notification"] = confirmation_shake
        collection.save(user)

        print u"Sent {} of {}.".format(sent, total)
        sent_mails.add(email)
        sent += 1


def generate_reg_ids(args):
    """
    Generate unique registration ids
    """
    db = DB(args.token)
    client = get_auth(db)

    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))

    for num, row in enumerate(rows.entry):
        info = row.to_dict()

        # update only
        if info.get("registrationid") is None:
            info["registrationid"] = REGID()
            row.from_dict(info)
            client.update(row)

        print "Generated `{registrationid}` for {email}".format(**info)


def sync_to_local_db(args):
    """
    Synchronize remote document with local mongo db
    """
    users = mongo_init().users
    db = DB(args.token)
    client = get_auth(db)

    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))

    for num, row in enumerate(rows.entry):
        info = row.to_dict()
        avail_user = users.find_one({"email": info["email"]})

        if not info["internalid"]:
            info["internalid"] = str(uuid.uuid4())

        if not avail_user:
            info["order"] = num
            users.insert(info)
            print "User {email} synced".format(**info)
        else:
            print "Updating {email}".format(**info)
            for key, val in info.iteritems():
                avail_user[key] = val
            print "User {email} updated".format(**info)
            users.save(avail_user)


def sync_from_local_db(args):
    """
    Synchronize local db with remote document
    """
    users = mongo_init().users
    db = DB(args.token)
    client = get_auth(db)

    sheet, wsheet = get_worksheet(client, doc_id=REGISTRATION_DOC_ID)
    rows = client.get_list_feed(ID(sheet), ID(wsheet.entry[0]))
    last = len(rows.entry)
    found_users = users.find({}).sort("order", pymongo.ASCENDING)

    #batch = gdata.spreadsheet.SpreadsheetsCellsFeed()

    for num, user in enumerate(found_users):
        row = dict([(key, val)
                    for key, val in user.iteritems()
                    if key != "_id"])

        order = row.pop("order", last)

        rows.entry[order].from_dict(row)
        #rows.entry[order].batch_id = BatchId('update-request')
        client.update(rows.entry[order])
        #batch.AddUpdate(rows.entry[order])

        if order >= last:
            last += 1

        print "Synced {}".format(row.get(u"email"))


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

parser.add_argument(
    "--confirmation", action="store_true", default=False,
    help="Send confirmation request")

parser.add_argument(
    "--campaign", default=None,
    help="Name of the campaign for confirmation (simple map)")

parser.add_argument(
    "--generate", action="store_true", default=False,
    help="Generate registrations ID")

parser.add_argument(
    "--sync_to_local", action="store_true", default=False,
    help="Sync data to local mongo server")

parser.add_argument(
    "--sync_from_local", action="store_true", default=False,
    help="Sync data from local mongo server to document")

args = parser.parse_args()


if args.auth:
    authenticate(args)
elif args.list:
    display_registrations(args)
elif args.send:
    send_registrations(args)
elif args.generate:
    generate_reg_ids(args)
elif args.sync_to_local:
    sync_to_local_db(args)
elif args.sync_from_local:
    sync_from_local_db(args)
elif args.confirmation:
    send_confirmation(args)
