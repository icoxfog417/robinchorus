"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb
from .group import Group
from .participant import Participant


class Chat(ndb.Model):
    group_key = ndb.KeyProperty(kind=Group)
    participant_key = ndb.KeyProperty(kind=Participant)
    message = ndb.TextProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_plain(self):
        group = Group.get_by_id(self.group_key.id())
        participant = Participant.get_by_id(self.participant_key.id())

        return {
            "group_name": group.name,
            "participant_name": participant.name,
            "message": self.message,
            "created_ymd": self.created_at.strftime('%Y/%m/%d'),
            "created_hms": self.created_at.strftime('%H:%M:%S')
        }
