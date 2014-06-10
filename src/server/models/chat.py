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

"""
class ChatPlain():
    def __init__(self, chat):
        group = Group.get_by_id(chat.group_key.id())
        participant = Participant.get_by_id(chat.participant_key.id())

        self.group_name = group.name
        self.participant_name = participant.name
        self.message = chat.message
        self.created_at = chat.created_at
"""