import tornado.web
import json
from models import Group


class GroupHandler(tornado.web.RequestHandler):

    def post(self):
        # get group name from request
        group_name = self.get_argument("groupName", "")
        response = {}

        if group_name:
            # create group
            group = Group(name=group_name)
            group.store()
            url = '{0}://{1}{2}'.format(self.request.protocol, self.request.host, "/chat/{0}".format(group.key))
            response = {"key": group.key, "url": url}

        return self.write(response)
