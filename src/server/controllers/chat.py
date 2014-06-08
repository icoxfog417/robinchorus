from flask import request,render_template,jsonify


class Chat:

    def __init__(self):
        pass

    @classmethod
    def index(cls,group):
        return render_template('chat.html')

    @classmethod
    def create(cls,group):
        return ""