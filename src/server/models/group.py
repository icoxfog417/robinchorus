"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class Group(ndb.Model):
    name = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
