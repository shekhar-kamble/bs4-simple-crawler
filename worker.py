import os
import traceback
from celery import Celery
from flask import Flask
from celery.utils.log import get_task_logger
from crawler import crawl
import json
from redis import Redis


broker_url = os.environ.get('AMQP_URL', 'amqp://')
app = Celery("worker",broker=broker_url, ignore_result=True, broker_heartbeat = None)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'crawl-tasks'
logger = get_task_logger(__name__)
server = Flask(__name__)
crawler_repo = Redis(
    host=os.environ.get('REDIS_DEFAULT_HOST','localhost'),
    port=os.environ.get('REDIS_DEFAULT_PORT',6379),
    db=0,
    password=os.environ.get('REDIS_DEFAULT_PASSWORD','')) 


@app.task()
def crawler_broker(public_id, crawl_url, depth):
    logger.info("start public_id={}".format(public_id))
    data = crawl(crawl_url, depth)
    crawler_repo.set(public_id+":data",json.dumps(data))
    logger.info("stop public_id={}".format(public_id))