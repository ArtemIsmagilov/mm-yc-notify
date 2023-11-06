import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from ..settings import envs

from dramatiq.middleware.asyncio import AsyncIO

rabbitmq_broker = RabbitmqBroker(url=envs.BROKER)
rabbitmq_broker.add_middleware(AsyncIO())
dramatiq.set_broker(rabbitmq_broker)
