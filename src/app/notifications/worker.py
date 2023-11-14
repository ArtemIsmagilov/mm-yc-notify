import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.stub import StubBroker

from settings import Conf

from dramatiq.middleware.asyncio import AsyncIO

if Conf.TESTING:
    broker = StubBroker()
else:
    broker = RabbitmqBroker(url=Conf.BROKER)

broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)
