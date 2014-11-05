import os
import tornado.web


class StampHandler(tornado.web.RequestHandler):

    def get(self, group_key):
        path = os.path.join(self.settings["static_path"],  "img", "stamps")
        stamps = {}
        for d in os.listdir(path):
            if os.path.isdir(os.path.join(path, d)):
                stamps[d] = []
                for f in os.listdir(os.path.join(path, d)):
                    stamps[d].append("/".join(["/static", "img", "stamps", d, f]))

        """
        stamp_def = {"default": range(1, 9), "sushiyuki": range(1, 41)}

        # can not read directory path on app engine server. so take this not good way
        for key in stamp_def:
            stamps[key] = list()
            for stamp_index in stamp_def[key]:
                stamps[key].append(path + key + "/stamp{num}.PNG".format(num=str(stamp_index).zfill(2)))
        """

        return self.write({"stamps": stamps})
