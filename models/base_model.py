import os
import json
from datetime import datetime
import redis


class BaseModel():

    def __init__(self, **kwargs):
        self.key = ""
        self.schema = self.__class__.__name__.lower()
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @classmethod
    def _dget(cls, key, args, default=""):
        if key in args:
            return args[key]
        else:
            return default

    @classmethod
    def create_connection(cls):
        redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
        connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)
        return connection

    def __format_key(self, key=None):
        if key:
            return ":".join([self.schema, key])
        else:
            return ":".join([self.schema])

    @classmethod
    def now(cls):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _store(self, hashed):
        c = self.create_connection()
        if not self.key:
            key_id = c.incr(self.__format_key())
            self.key = self.__format_key(str(key_id))

        serialized = json.dumps(hashed)
        c.set(self.key, serialized)

    @classmethod
    def get(cls, key):
        instance = cls()
        instance.key = key
        if key:
            c = cls.create_connection()
            serialized = c.get(key)
            hased = json.loads(serialized)
            for k in hased:
                if hased[k]:
                    setattr(instance, k, hased[k])

        return instance

    def delete(self):
        if self.key:
            c = self.create_connection()
            c.delete(self.key)

    def _list_name(self, property_name):
        if self.key:
            return "{0}:{1}".format(self.key, property_name)
        else:
            raise Exception("Can not access to the list property {0}. Because key is None".format(property_name))

    def push_list(self, list_name, obj):
        c = self.create_connection()
        c.lrem(list_name, 0, obj.key)  # erase duplicate
        c.lpush(list_name, obj.key)

    def get_list(self, list_name, model_class, start=0, count=1):
        c = self.create_connection()
        mks = c.lrange(list_name, start, count-1)
        models = []
        for k in mks:
            models.append(model_class.get(k))

        return models
