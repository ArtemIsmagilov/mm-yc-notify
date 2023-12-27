from dramatiq.middleware import Prometheus
import dramatiq, os
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from settings import Conf


# dramatiq app.notifications.tasks
def remove_prometheus(b: RabbitmqBroker):
    for m in b.middleware:
        if type(m) is Prometheus:
            b.middleware.remove(m)
            break


broker = RabbitmqBroker(url=Conf.BROKER)

dramatiq.set_broker(broker)

dramatiq.get_broker().add_middleware(AsyncIO())

remove_prometheus(dramatiq.get_broker())
