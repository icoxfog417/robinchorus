from flask import request,jsonify


class Group:

    def __init__(self):
        pass

    @classmethod
    def create(cls):
        group = request.form.get("group", "", type=str)
        if group != "":
            # create group
            id  = "xxxxxxx"
            url = request.url_root + "chat/" + id
            return jsonify(id = id, url=url)
        else:
            return ""