from settings import Conf

# worker_class = 'gthread'
# workers = multiprocessing.cpu_count() * 2 + 1
# threads = multiprocessing.cpu_count() * 2 + 1

bind = [f"{Conf.APP_HOST_EXTERNAL}:{Conf.APP_PORT_EXTERNAL}"]
accesslog = '-'
access_log_format = 'h:%(h)s l:%(l)s u:%(u)s t:%(t)s r:"%(r)s" s:%(s)s b:%(b)s f:"%(f)s" a:"%(a)s"\n________________\n'
errorlog = '-'
loglevel = 'debug'
wsgi_app = "app:create_app()"
worker_class = 'uvicorn.workers.UvicornWorker'

# certfile = '/etc/letsencrypt/live/www.example.com/fullchain.pem'
# keyfile = '/etc/letsencrypt/live/www.example.com/privkey.pem'
# ssl_version =  # if necessary
# print_config = True
# check_config = True
