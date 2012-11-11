
import datetime
import uuid

from db import mongo_init


__all__ = ("REGID", "add_user")


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
