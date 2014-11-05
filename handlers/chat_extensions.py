import os
import tornado.web


class StampHandler(tornado.web.RequestHandler):

    def get(self, group_key):
        path = os.path.join(self.settings["static_path"],  "img", "stamps")
        stamps = {}
        for d in sorted(os.listdir(path)):
            if os.path.isdir(os.path.join(path, d)):
                stamps[d] = []
                for f in sorted(os.listdir(os.path.join(path, d))):
                    stamps[d].append("/".join(["/static", "img", "stamps", d, f]))

        return self.write({"stamps": stamps})
