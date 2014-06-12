from flask import request, jsonify
from server.models import Group
from urlparse import urljoin


class GroupController:

    def __init__(self):
        pass

    @classmethod
    def create(cls):
        # get group name from request
        group_name = request.form.get("groupName", u"", type=unicode)

        if group_name != "":
            # create group
            group = Group(name=group_name)
            group_key = group.put()

            group_id = group_key.id()
            url = request.url_root + "chat/" + str(group_id)

            return jsonify(id=group_id, url=url)
        else:
            return ""