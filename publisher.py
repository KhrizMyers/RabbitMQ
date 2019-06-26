import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='test')

for i in range(1, 10):
    channel.basic_publish(exchange='', routing_key='test', body=str(i))

print('[X] Sent')
connection.close()

