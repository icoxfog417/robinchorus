"""
environments.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""

from datetime import datetime, timedelta
import calendar


class Config(object):
    # Flask-Cache settings
    CACHE_TYPE = 'gaememcached'
    COOKIE_EXPIRATION = timedelta(hours=2)

    @classmethod
    def calculate_expiration(cls):
        endpoint = datetime.utcnow() + cls.COOKIE_EXPIRATION
        return calendar.timegm(endpoint.timetuple())


class Development(Config):
    DEBUG = True
    # Flask-DebugToolbar settings
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CSRF_ENABLED = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    CSRF_ENABLED = True


class Production(Config):
    DEBUG = False
    CSRF_ENABLED = True