from flask import request, render_template, make_response, jsonify
from google.appengine.api import channel
from server.models import Group, Participant, Chat
import json
import os


class ChatController:

    def __init__(self):
        pass

    @classmethod
    def index(cls, group_id):
        # confirm participant id in cookie
        c_group_id = request.cookies.get("group_id")
        participant_id = request.cookies.get("participant_id")

        # if participant is none or login to another group, create new participant in group
        if not participant_id or c_group_id != str(group_id):
            # get group
            group = Group.get_by_id(group_id)

            # create new participant todo:consider the case that group is None
            participant = Participant()
            participant.group_key = group.key
            participant_id = participant.put().id()  # save it to datastore

        # create channel
        token = channel.create_channel(str(participant_id))

        # return response
        resp = make_response(render_template('chat.html', token=token))

        # set participant_id to cookie
        resp.set_cookie("group_id", str(group_id))
        resp.set_cookie("participant_id", str(participant_id))

        return resp

    @classmethod
    def find(cls, group_id):
        group = Group.get_by_id(group_id)
        chats = Chat.query(Chat.group_key == group.key).order(-Chat.created_at).fetch(100)
        return jsonify(chats=list(map(lambda c: c.to_dict(), chats)))

    @classmethod
    def create(cls, group_id, msg_type):
        group = Group.get_by_id(group_id)
        participant_key = None
        participant_id = request.cookies.get("participant_id")

        if participant_id:
            participant_key = Participant.get_by_id(long(participant_id)).key

        message = request.form.get("message", u"", type=unicode)
        reference_id = request.form.get("reference", u"", type=unicode)

        chat = Chat(
            group_key=group.key,
            participant_key=participant_key,
            type=msg_type,
            message=message
        )

        #set reference if exist
        if reference_id:
            reference = Chat.get_by_id(long(reference_id))
            if reference is not None:
                chat.reference = reference.key.id()

        chat.put()

        # send same group members (include myself)
        cls.__broadcast(group_id, chat)

        # message is send by channel, so you don't need return
        return ""

    @classmethod
    def update(cls, group_id, update_func):
        chat_id = request.form.get("id", u"", type=unicode)
        if chat_id:
            chat = Chat.get_by_id(long(chat_id))
            if chat is not None:
                update_func(chat)
                chat.put()
                cls.__broadcast(group_id, chat)

        return ""

    @classmethod
    def __broadcast(cls, group_id, chat):
        group = Group.get_by_id(group_id)
        participants_in_group = Participant.query(Participant.group_key == group.key)
        send = lambda p: channel.send_message(str(p.key.id()), json.dumps(chat.to_dict()))
        map(send, participants_in_group)

    @classmethod
    def find_stamps(cls, group_id):
        path = "/server/assets/img/stamps/"
        stamps = []
        for num in range(1, 8):
            stamps.append(path + "stamp{num}.PNG".format(num=str(num).zfill(2)))

        return jsonify(stamps=stamps)
