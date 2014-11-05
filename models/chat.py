from base_model import BaseModel
from group import Group


class Chat(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.participant_key = super()._dget("participant_key", kwargs)
        self.type = super()._dget("type", kwargs)
        self.message = super()._dget("message", kwargs)
        self.like = super()._dget("like", kwargs, 0)
        self.reference = super()._dget("reference", kwargs)
        self.created_at = super()._dget("created_at", kwargs)
        self.visible = "1"

    def store(self, group_key=None, participant_key=None):
        def save(is_created=True):
            if is_created:
                self.created_at = self.now()
            data = self._to_dict()
            self._store(data)

        if group_key and participant_key:
            # store chat
            self.participant_key = participant_key
            save()

            # store to grouop
            g = Group.get(group_key)
            g.chat(self)
        elif self.key:
            save(False)

    def _to_dict(self):
        data = {
            "key": self.key,
            "participant_key": self.participant_key,
            "type": self.type,
            "message": self.message,
            "like": self.like,
            "reference": self.reference,
            "created_at": self.created_at,
            "visible": self.visible
        }
        return data

    def to_dict(self):
        data = self._to_dict()
        from participant import Participant
        participant = Participant.get(self.participant_key)
        data["participant_name"] = participant.name

        return data
