"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb
from .group import Group


class Participant(ndb.Model):
    group_key = ndb.KeyProperty(kind=Group)
    name = ndb.StringProperty()
    joined_at = ndb.DateTimeProperty(auto_now_add=True)
