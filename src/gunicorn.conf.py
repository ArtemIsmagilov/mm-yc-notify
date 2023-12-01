import multiprocessing
from settings import Conf

worker_class = 'uvicorn.workers.UvicornWorker'
workers = multiprocessing.cpu_count() * 2 + 1
# threads = multiprocessing.cpu_count() * 2 + 1

bind = [f"0.0.0.0:{Conf.APP_PORT_EXTERNAL}"]
access_log_format = 'h:%(h)s l:%(l)s u:%(u)s t:%(t)s r:"%(r)s" s:%(s)s b:%(b)s f:"%(f)s" a:"%(a)s"\n________________\n'
# capture_output = True
# daemon = True
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
wsgi_app = "app:create_app()"


# certfile = '/etc/letsencrypt/live/www.example.com/fullchain.pem'
# keyfile = '/etc/letsencrypt/live/www.example.com/privkey.pem'
# ssl_version =  # if necessary
# print_config = True
# check_config = True
