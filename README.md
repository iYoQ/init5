# init5


docker run --name=your_name -d -p 6379:6379 redis

celery -A config worker -l info --pool=gevent

celery -A config flower --port=5566
