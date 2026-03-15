from configuration import r

pubsub = r.pubsub()
pubsub.subscribe('__keyevent@__:lpop')

for message in pubsub.listen():
    if message['type'] == 'message':
        r.save()

