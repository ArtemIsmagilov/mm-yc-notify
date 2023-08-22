import dotenv, os

dotenv.load_dotenv()

APP_SCHEMA = os.environ['APP_SCHEMA']
APP_HOST_INTERNAL = os.environ['APP_HOST_INTERNAL']
APP_PORT_INTERNAL = os.environ['APP_PORT_INTERNAL']

APP_HOST_EXTERNAL = os.environ['APP_HOST_EXTERNAL']
APP_PORT_EXTERNAL = os.environ['APP_PORT_EXTERNAL']

APP_URL_INTERNAL = os.environ['APP_URL_INTERNAL']
APP_URL_EXTERNAL = os.environ['APP_URL_EXTERNAL']

STATIC_PATH = os.environ['STATIC_PATH']

CHECK_EVENTS = os.environ['CHECK_EVENTS']


# flask config
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True if os.environ['DEBUG'].lower() in ('true', 'y', 'yes',) else False
TESTING = True if os.environ['TESTING'].lower() in ('true', 'y', 'yes',) else False

# mm config
MM_SCHEMA = os.environ['MM_SCHEMA']
MM_HOST_EXTERNAL = os.environ['MM_HOST_EXTERNAL']
MM_PORT_EXTERNAL = os.environ['MM_PORT_EXTERNAL']

MM_URL_EXTERNAL = os.environ['MM_URL_EXTERNAL']

MM_APP_TOKEN = os.environ['MM_APP_TOKEN']

MM_BOT_OPTIONS = {
    'scheme': MM_SCHEMA,
    'url': MM_HOST_EXTERNAL,
    'port': int(MM_PORT_EXTERNAL),
    'token': MM_APP_TOKEN,
    #'debug': DEBUG,
}

DB_DSN = os.environ['DB_DSN']

DB_URL = os.environ['DB_URL']
