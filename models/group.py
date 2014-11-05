from .base_model import BaseModel


class Group(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = super()._dget("name", kwargs)

    def __chat_list(self):
        if self.key:
            return self.key + ":chat"
        else:
            raise Exception("Can not access to the group's chats. Because group key is None")

    def store(self):
        data = {
            "name": self.name
        }
        self._store(data)

    def chat(self, chat):
        return self.push_list(self._list_name("chat"), chat)

    def chats(self, start=0, count=1):
        from .chat import Chat
        return self.get_list(self._list_name("chat"), Chat, start, count)

    def participant(self, participant):
        return self.push_list(self._list_name("participant"), participant)

    def participants(self, start=0, count=1):
        from .participant import Participant
        return self.get_list(self._list_name("participant"), Participant, start, count)
