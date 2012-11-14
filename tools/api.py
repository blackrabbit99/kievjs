
import datetime
import uuid

import settings
from db import mongo_init
from codes import generate_code, generate_badge

__all__ = ("REGID", "add_user")


CONFIRMATION_URL = getattr(settings, "CONFIRMATION_URL", "")
REGISTRATION_URL = getattr(settings, "REGISTRATION_URL", "")
BADGE_TITLE = getattr(settings, "BADGE_TITLE", "")


REGID = lambda: "-".join(str(uuid.uuid4()).split("-")[:2])


def add_user(**kwargs):
    # defined data structure
    data = dict(
        registrationid=None,
        name=None,
        internalid=None,
        timestamp=None,
        comments=None,
        company=None,
        confirmationshake1=None,
        confirmationshake2=None,
        email=None,
        passed=None,
        notification=None,
        position=None,
        order=None)

    data.update(kwargs)

    if not data.get("internalid"):
        # generate internal id
        data["internalid"] = str(uuid.uuid4())

    if not data.get("timestamp"):
        # generate timestamp: 9/27/2012 9:45:15
        data["timestamp"] = datetime.datetime.now().strftime(
            "%m/%d/%Y %H:%M:%S")

    if not data.get("registrationid"):
        # generate registration ID
        data["registrationid"] = REGID()

    if not data.get("name") or not data.get("email"):
        raise ValueError(
            "Name and Email are required fields")

    mongo_init().users.insert(data)

    return data


def generate_confirmation(internal_id):
    """
    Generate PDF with confirmation
    """
    # prepare context
    users = mongo_init().users
    user = users.find_one({"internalid": internal_id})

    registration_link = REGISTRATION_URL.format(
        user["registrationid"])

    code = generate_code(
        registration_link,
        output="build/codes/{}.png".format(internal_id))
    value_or_empty = lambda key: user.get(key, "") or ""

    if not user.get("registrationid", None):
        return None

    badge = generate_badge(
        title=BADGE_TITLE,
        name=value_or_empty("name").strip(),
        company=value_or_empty("company").strip(),
        position=value_or_empty("position").strip(),
        qr_code=code,
        reg_id=user.get("registrationid"),
        output="build/{}.pdf".format(internal_id))

    return badge
