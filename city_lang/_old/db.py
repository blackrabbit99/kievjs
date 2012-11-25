import base64
import json
import os
import pymongo

from Crypto.Cipher import ARC4

DB_FILE = ".kjsdb"
MONGO_DATABASE = "kjs_conference"


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


def mongo_init():
    """
    Create connection to mongo database and return it
    """
    connection = pymongo.Connection()
    return connection[MONGO_DATABASE]
