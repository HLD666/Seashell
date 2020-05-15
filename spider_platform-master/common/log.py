import os
import logging
import datetime
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

day_str = datetime.datetime.now().strftime("%Y%m%d")
log_format = logging.Formatter('%(asctime)s %(process)d %(thread)d %(filename)s %(lineno)d %(levelname)s: %(message)s',
                               datefmt='%Y-%m-%d %H:%M:%S')

rt_handler = RotatingFileHandler(os.path.join(BASE_DIR, f"log_{day_str}.log"), maxBytes=5*1024*1024, backupCount=1)
# rt_handler.setLevel(logging.INFO)
rt_handler.setLevel(logging.DEBUG)
rt_handler.setFormatter(log_format)

console = logging.StreamHandler()
console.setLevel(logging.CRITICAL)
console.setFormatter(log_format)

log = logging.getLogger('CRAWL')
# log.setLevel("INFO")
log.setLevel("DEBUG")
log.addHandler(rt_handler)
log.addHandler(console)

debug = log.debug
info = log.info
warning = log.warning
error = log.error
critical = log.critical
