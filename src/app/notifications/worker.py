import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import Conf

from dramatiq.middleware.asyncio import AsyncIO

broker = RabbitmqBroker(url=Conf.BROKER)

broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)
