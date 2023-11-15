import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.middleware.prometheus import Prometheus
from settings import Conf


def remove_prometheus(b: RabbitmqBroker):
    for m in b.middleware:
        if type(m) is Prometheus:
            b.middleware.remove(m)
            break


broker = RabbitmqBroker(url=Conf.BROKER)
remove_prometheus(broker)
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)
