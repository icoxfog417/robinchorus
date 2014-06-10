from flask import request, render_template, jsonify
from google.appengine.api import channel
from server.models import Group, Participant, Chat
import cgi


class ChatController:

    def __init__(self):
        pass

    @classmethod
    def index(cls, group_id):
        # confirm participant id in cookie
        c_group_id = request.cookies.get("group_id")
        participant_id = request.cookies.get("participant_id")

        # if participant is none or login to another group, create new participant in group
        if not participant_id or c_group_id != group_id:
            # get group
            group = Group.get_by_id(group_id)

            # create new participant todo:consider the case that group is None
            participant = Participant()
            participant.group_key = group.key
            participant_id = participant.put().id()  # save it to datastore

        # create channel
        token = channel.create_channel(participant_id)

        # return response
        resp = render_template('chat.html', token=token)

        # set participant_id to cookie
        resp.set_cookie("group_id", group_id)
        resp.set_cookie("participant_id", participant_id)

        return resp

    @classmethod
    def find(cls, group_id):
        group = Group.get_by_id(group_id)
        chats = Chat.query(group_key=group.key()).order(-Chat.created_at).fetch(100)
        return jsonify(chats=chats)

    @classmethod
    def create(cls, group_id):
        group = Group.get_by_id(group_id)
        participant_key = None
        participant_id = request.cookies.get("participant_id")
        if participant_id:
            participant_key = Participant.get_by_id(participant_id).key()

        message = request.form.get("message", "", type=str)
        message = cgi.escape(message)  # escape the string

        chat = Chat(
            group_key=group.key(),
            participant_key=participant_key,
            message=message
        )

        chat.put()

        # send same group members (include myself)
        participants_in_group = Participant.query(group_key=group.key())
        send = lambda p: channel.send_message(p.key().id(), chat)
        map(participants_in_group, send)

        # message is send by channel, so you don't need return
        return ""