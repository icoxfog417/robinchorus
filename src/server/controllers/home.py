from flask import render_template


class Home:

    def __init__(self):
        pass

    @classmethod
    def index(cls):
        return render_template('index.html')
