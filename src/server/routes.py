"""
urls.py

URL dispatch route mappings and error handlers

"""
from server import app
from server import controllers
from flask import render_template

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
    return controllers.Home.index()

@app.route("/_group", methods=['POST'])
def group_create():
   return controllers.Group.create()

@app.route("/chat/<string:group>", methods=['GET'])
def chat_index(group):
    return controllers.Chat.index(group)

@app.route("/chat/<string:group>", methods=['POSTs'])
def chat_create(group):
    return controllers.Chat.create(group)

# Say hello
#app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)

# Examples list page
#app.add_url_rule('/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# Examples list page (cached)
#app.add_url_rule('/examples/cached', 'cached_examples', view_func=views.cached_examples, methods=['GET'])

# Contrived admin-only view example
#app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# Edit an example
#app.add_url_rule('/examples/<int:example_id>/edit', 'edit_example', view_func=views.edit_example, methods=['GET', 'POST'])

# Delete an example
#app.add_url_rule('/examples/<int:example_id>/delete', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
