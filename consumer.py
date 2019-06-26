import random

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='test')


def callback(ch, method, properties, body):
    r = random.randint(1, 11)
    time.sleep(r)
    print(f'[X] received {body.decode()} in {r} seconds')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=callback)

print('Waiting for a message')
channel.start_consuming()
