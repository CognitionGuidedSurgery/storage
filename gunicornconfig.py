import multiprocessing
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1

#max_requests = 1024
#preload_app = True
#pidfile = "/tmp/gunicorn.pid"
accesslog = "-" # stderr
errorlog = "-" # stderr
