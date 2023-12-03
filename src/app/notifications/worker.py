from taskiq_aio_pika import AioPikaBroker
from taskiq import InMemoryBroker
from settings import Conf

# taskiq worker app.notifications.worker:broker --fs-discover
if Conf.TESTING:
    broker = InMemoryBroker()
else:
    broker = AioPikaBroker(Conf.BROKER)
