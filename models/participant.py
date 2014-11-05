from base_model import BaseModel
from group import Group


class Participant(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ""

    def store(self, group_key):
        data = {
            "name": self.name
        }
        self._store(data)

        g = Group.get(group_key)
        g.participant(self)
