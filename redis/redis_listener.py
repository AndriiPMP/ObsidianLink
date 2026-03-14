import redis

r = redis.Redis(host='localhost', port=6379, db=0)

pubsub = r.pubsub()
pubsub.subscribe('__keyevent@__:lpop')

for message in pubsub.listen():
    if message['type'] == 'message':
        r.save()

