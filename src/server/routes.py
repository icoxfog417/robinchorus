"""
urls.py

URL dispatch route mappings and error handlers

"""
from server import app
from server import controllers
from flask import request, render_template

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

@app.route("/_ah/warmup")
def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

# Home page
@app.route("/")
def home_index():
    return controllers.HomeController.index()

@app.route("/_group", methods=['POST'])
def group_create():
    return controllers.GroupController.create()

@app.route("/chat/<int:group_id>")
def chat_index(group_id):
    return controllers.ChatController.index(group_id)

@app.route("/chat/<int:group_id>/_find", methods=['GET'])
def chat_find(group_id):
    return controllers.ChatController.find(group_id)

@app.route("/chat/<int:group_id>", methods=['POST'])
def chat_create(group_id):
    msg_type = request.form.get("type", u"", type=unicode)

    if msg_type == u"like":
        def update_like(c):
            if c.like is None:
                c.like = 1
            else:
                c.like += 1

        return controllers.ChatController.update(group_id, update_like)
    else:
        return controllers.ChatController.create(group_id, msg_type)

@app.route("/chat/<int:group_id>/_stamps", methods=['POST'])
def chat_find_stamps(group_id):
    return controllers.ChatController.find_stamps(group_id)

"""
@app.route("/chat/<int:group_id>/_reconnect_channel", methods=['POST'])
def reconnect_channel(group_id):
    return controllers.ChatController.reconnect_channel(group_id)
"""

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
