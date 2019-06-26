import json

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

type_message = "".join(sys.argv[1]) or "Hello world"
message = "".join(sys.argv[2])

dic = {
    'type_message': type_message,
    'message': message
}


channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(dic))

print('[X] Sent')
connection.close()
