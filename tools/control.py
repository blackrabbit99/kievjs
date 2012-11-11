import argparse
import hashlib
import pymongo

from db import mongo_init


def users(args):
    """
    List of users
    """
    auth = mongo_init().auth
    users = auth.find({}).sort("username", pymongo.ASCENDING)

    for user in users:
        print "User: {username}".format(**user)


def add(args):
    """
    Add new user
    """
    auth = mongo_init().auth

    if not args.username or not args.password:
        raise ValueError("Please, enter --username "
                         "and --password for new user")

    md5 = hashlib.md5()
    md5.update(args.password)

    new_user = {
        "username": args.username,
        "password": md5.hexdigest()
    }

    if auth.find_one({"username": args.username}):
        raise ValueError("Username `{}` already available".format(
            args.username))

    auth.insert(new_user)
    print "User {username} added".format(**new_user)


def change(args):
    """
    Change password
    """
    auth = mongo_init().auth

    if not args.username or not args.password:
        raise ValueError("Please, enter --username "
                         "and --password for new user")

    user = auth.find_one({"username": args.username})

    if not user:
        raise ValueError("Username `{}` not exist yet".format(
            args.username))

    md5 = hashlib.md5()
    md5.update(args.password)

    user["password"] = md5.hexdigest()
    auth.save(user)

    print "Password for `{username}` changed".format(**user)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manipulate authentication")

    parser.add_argument(
        "--list", action="store_true", default=False,
        help="Show users")

    parser.add_argument(
        "--add", action="store_true", default=False,
        help="Add new user")

    parser.add_argument(
        "--change", action="store_true", default=False,
        help="Change password for particular user")

    parser.add_argument(
        "--username", default=None,
        help="Username")

    parser.add_argument(
        "--password", default=None,
        help="Password")

    args = parser.parse_args()

    if args.list:
        users(args)
    if args.add:
        add(args)
    if args.change:
        change(args)
