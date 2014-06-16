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
    type = ndb.StringProperty()
    message = ndb.TextProperty()
    like = ndb.IntegerProperty()
    reference = ndb.IntegerProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        group = Group.get_by_id(self.group_key.id())
        participant = Participant.get_by_id(self.participant_key.id())

        return {
            "id": self.key.id(),
            "group_name": group.name,
            "participant_name": participant.name,
            "type": self.type,
            "message": self.message,
            "like": self.like,
            "reference": self.reference,
            "created_timestamp": self.created_at.strftime('%Y/%m/%d') + " " + self.created_at.strftime('%H:%M:%S'),
            "visible": "1"
        }
