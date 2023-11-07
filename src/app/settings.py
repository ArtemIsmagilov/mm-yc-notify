import dotenv, os
from abc import ABC, abstractmethod


class Conf(ABC):
    @abstractmethod
    def __init__(self, filename: str):
        path_dotenv = dotenv.find_dotenv(filename)
        dotenv.load_dotenv(path_dotenv)

        self.APP_SCHEMA = os.environ['APP_SCHEMA']
        self.APP_HOST_INTERNAL = os.environ['APP_HOST_INTERNAL']
        self.APP_PORT_INTERNAL = os.environ['APP_PORT_INTERNAL']

        self.APP_HOST_EXTERNAL = os.environ['APP_HOST_EXTERNAL']
        self.APP_PORT_EXTERNAL = os.environ['APP_PORT_EXTERNAL']

        self.APP_URL_INTERNAL = os.environ['APP_URL_INTERNAL']
        self.APP_URL_EXTERNAL = os.environ['APP_URL_EXTERNAL']

        self.CHECK_EVENTS = int(os.environ['CHECK_EVENTS'])

        # quart config
        self.SECRET_KEY = os.environ['SECRET_KEY']
        self.DEBUG = True if os.environ['DEBUG'].lower() in ('true', 'y', 'yes',) else False
        self.TESTING = True if os.environ['TESTING'].lower() in ('true', 'y', 'yes',) else False

        # dramatiq config
        self.BROKER = os.environ['BROKER']

        # mm config
        self.MM_SCHEMA = os.environ['MM_SCHEMA']
        self.MM_HOST_EXTERNAL = os.environ['MM_HOST_EXTERNAL']
        self.MM_PORT_EXTERNAL = os.environ['MM_PORT_EXTERNAL']

        self.MM_URL_EXTERNAL = os.environ['MM_URL_EXTERNAL']

        self.MM_APP_TOKEN = os.environ['MM_APP_TOKEN']

        self.MM_BOT_OPTIONS = {
            'scheme': self.MM_SCHEMA,
            'url': self.MM_HOST_EXTERNAL,
            'port': int(self.MM_PORT_EXTERNAL),
            'token': self.MM_APP_TOKEN,
            # 'debug': self.DEBUG,
        }

        # DB
        self.DB_URL = os.environ['DB_URL']


class Dev(Conf):
    def __init__(self, filename='.dev.env'):
        super().__init__(filename)


class Prod(Conf):
    def __init__(self, filename='.env'):
        super().__init__(filename)


class Testing(Conf):
    def __init__(self, filename='.test.env'):
        super().__init__(filename)
        # testing client
        self.test_client_email = os.environ['test_client_email']
        self.test_client_username = os.environ['test_client_username']
        self.test_client_first_name = os.environ['test_client_first_name']
        self.test_client_last_name = os.environ['test_client_last_name']
        self.test_client_nickname = os.environ['test_client_nickname']
        self.test_client_password = os.environ['test_client_password']
        # testings yandex calendar params
        self.test_client_ya_login = os.environ['test_client_ya_login']
        self.test_client_ya_token = os.environ['test_client_ya_token']
        self.test_client_ya_timezone = os.environ['test_client_ya_timezone']


envs = Prod()
