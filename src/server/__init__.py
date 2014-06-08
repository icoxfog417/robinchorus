"""
Initialize Flask app

"""
from flask import Flask
import os
from werkzeug.debug import DebuggedApplication
views = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')

app = Flask(__name__,template_folder=views)

if os.getenv('FLASK_CONF') == 'DEV':
    #development environments n
    app.config.from_object('server.environments.Development')

    # Google app engine mini profiler
    # https://github.com/kamens/gae_mini_profiler
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    from gae_mini_profiler import profiler, templatetags 
    @app.context_processor
    def inject_profiler():
        return dict(profiler_includes=templatetags.profiler_includes())
    app.wsgi_app = profiler.ProfilerWSGIMiddleware(app.wsgi_app)

elif os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('server.environments.Testing')

else:
    app.config.from_object('server.environments.Production')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Pull in URL dispatch routes
import routes
