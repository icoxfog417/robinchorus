from datetime import datetime, timedelta
import calendar
import tornado.web
import tornado.websocket
import tornado.escape as escape
from models import Group, Participant, Chat


class ChatsHandler(tornado.web.RequestHandler):
    def get(self, group_key):
        group = Group.get(group_key)
        chats = group.chats(0, 300)
        return self.write({"chats": list(map(lambda c: c.to_dict(), chats))})


class ChatTrait():
    COOKIE_EXPIRATION = timedelta(hours=3)
    GROUP_KEY = "group_key"
    PARTICIPANT_KEY = "participant_key"

    @classmethod
    def calculate_expiration(cls):
        endpoint = datetime.utcnow() + cls.COOKIE_EXPIRATION
        return calendar.timegm(endpoint.timetuple())

    @classmethod
    def get_group_key(cls, handler):
        return escape.to_unicode(handler.get_secure_cookie(ChatTrait.GROUP_KEY))

    @classmethod
    def get_participant_key(cls, handler):
        return escape.to_unicode(handler.get_secure_cookie(ChatTrait.PARTICIPANT_KEY))

    @classmethod
    def store_group_key(cls, handler, value):
        handler.set_secure_cookie(ChatTrait.GROUP_KEY, value, expires=cls.calculate_expiration())

    @classmethod
    def store_participant_key(cls, handler, value):
        handler.set_secure_cookie(ChatTrait.PARTICIPANT_KEY, value, expires=cls.calculate_expiration())


class ChatHandler(tornado.web.RequestHandler):

    def get(self, group_key):
        # confirm participant id in cookie
        c_group_key = ChatTrait.get_group_key(self)
        participant_key = ChatTrait.get_participant_key(self)

        # get group
        group = Group.get(group_key)

        # if participant is none or login to another group, create new participant in group
        if not participant_key:
            participant = Participant()
            participant.store(group.key)
            participant_key = participant.key
            ChatTrait.store_participant_key(self, participant_key)

        if c_group_key:
            if c_group_key != group_key:
                group.participant(Participant.get(participant_key))
                ChatTrait.store_group_key(self, group.key)
        else:
            ChatTrait.store_group_key(self, group.key)

        # return response
        self.render("chat.html", group_name=group.name)

    def post(self, group_key):
        participant_key = ChatTrait.get_participant_key(self)

        msg_type = self.get_argument("type", "")
        message = self.get_argument("message", "")
        reference = self.get_argument("reference", "")

        chat = Chat(
            type=msg_type,
            message=message
        )

        #set reference if exist
        if reference:
            reference = Chat.get(reference)
            if reference is not None:
                chat.reference = reference.key

        chat.store(group_key, participant_key)

        # send same group members (include myself)
        ChatSocketHandler.broadcast(group_key, chat)

        return self.write({})

    def put(self, group_key):
        chat_key = self.get_argument("key", u"")
        update_type = self.get_argument("type", u"")
        chat = Chat.get(chat_key)

        if chat:
            if update_type == "like":
                chat.like += 1

            chat.store()
            ChatSocketHandler.broadcast(group_key, chat)

        return self.write({})


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = {}

    def open(self, group_key):
        gkey = ChatTrait.get_group_key(self)
        if not gkey in ChatSocketHandler.waiters:
            ChatSocketHandler.waiters[gkey] = set()
        ChatSocketHandler.waiters[gkey].add(self)

    def on_close(self):
        gkey = ChatTrait.get_group_key(self)
        if gkey and gkey in ChatSocketHandler.waiters:
            ChatSocketHandler.waiters[gkey].remove(self)

    def on_message(self, message):
        pass

    @classmethod
    def broadcast(cls, group_key, chat):
        if group_key in ChatSocketHandler.waiters:
            for waiter in cls.waiters[group_key]:
                try:
                    waiter.write_message(chat.to_dict())
                except:
                    pass
