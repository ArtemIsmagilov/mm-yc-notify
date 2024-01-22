import dotenv
import os
import logging

dotenv.load_dotenv()


class Conf:
    APP_SCHEMA = os.environ['APP_SCHEMA']
    APP_HOST_INTERNAL = os.environ['APP_HOST_INTERNAL']
    APP_PORT_INTERNAL = os.environ['APP_PORT_INTERNAL']

    APP_HOST_EXTERNAL = os.environ['APP_HOST_EXTERNAL']
    APP_PORT_EXTERNAL = os.environ['APP_PORT_EXTERNAL']

    APP_URL_INTERNAL = os.environ['APP_URL_INTERNAL']
    APP_URL_EXTERNAL = os.environ['APP_URL_EXTERNAL']

    CHECK_EVENTS = int(os.environ['CHECK_EVENTS'])
    RANGE_DAYS = int(os.environ['RANGE_DAYS'])

    # quart config
    QUART_APP = os.environ['QUART_APP']
    SECRET_KEY = os.environ['SECRET_KEY']
    LOG_LEVEL = int(os.environ['LOG_LEVEL'])
    TESTING = True if os.environ['TESTING'].lower() in ('true', 'y', 'yes',) else False

    # dramatiq config
    BROKER = os.environ['BROKER']

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
        # 'debug': LOG_LEVEL == 10,
    }

    # DB
    DB_URL = os.environ['DB_URL']


class Testing(Conf):
    # testing client
    test_client_email = os.environ['test_client_email']
    test_client_username = os.environ['test_client_username']
    test_client_first_name = os.environ['test_client_first_name']
    test_client_last_name = os.environ['test_client_last_name']
    test_client_nickname = os.environ['test_client_nickname']
    test_client_password = os.environ['test_client_password']
    # testings yandex calendar params
    test_client_ya_login = os.environ['test_client_ya_login']
    test_client_ya_token = os.environ['test_client_ya_token']
    test_client_ya_timezone = os.environ['test_client_ya_timezone']
    # test yandex calendars
    test_client_calendar_name1 = os.environ['test_client_calendar_name1']
    test_client_calendar_name2 = os.environ['test_client_calendar_name2']


logging.basicConfig(
    level=Conf.LOG_LEVEL,
    format='%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(msg)s',
    datefmt='%d-%m-%Y %H:%M:%S %Z'
)
