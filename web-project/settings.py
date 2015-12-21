import os

_ROOT = os.path.dirname(__file__)

TITLE = "SSDUT BASKETBALL"
SUB_TITLE = "SSDUT BASKETBALL"
DOMAIN_NAME = "basketball.SSDUT.cn"
HANDLERS = (
    'web',
)

LOGIN_URL = "/login"
COOKIE_SECRET = "/hncZPV7TVaxY/krcQFc9Ujm6blLPk9Bsh6xdIYfAuc="

MYSQL_HOST = 'localhost'
MYSQL_DATABASE_NAME = 'SSDUT'
MYSQL_USER_NAME = 'root'
MYSQL_PASS_WORD = 'ssdut'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

WEBMASTER = ''
ADMIN_EMAILS = []

DEFAULT_DATABASE_NAME = 'SSDUT'

OAUTH_SETTINGS = {
    'client_id': '',
    'client_secret': '',
    'base_url': '',
    'redirect_url': ''
}

try:
    from local_settings import *
except ImportError:
    pass
