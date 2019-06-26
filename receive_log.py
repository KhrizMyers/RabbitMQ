from local_settings import HideSettings
import pika
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result_queue = channel.queue_declare(queue='', exclusive=True)

queue_name = result_queue.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    dic = eval(body.decode())

    if dic['type_message'] == 'debug' or dic['type_message'] == 'info' or dic['type_message'] == 'warning' \
            or dic['type_message'] == 'error':
        message = open('/home/christianz/PycharmProjects/RabbitMQ/debug.txt', 'a+')
        message.write(dic['message'] + '\n')
        message.close()
        print(f'[X] received {dic}')
        send_email(dic)

    if dic['type_message'] == 'info' or dic['type_message'] == 'warning' or dic['type_message'] == 'error':
        message = open('/home/christianz/PycharmProjects/RabbitMQ/info.txt', 'a+')
        message.write(dic['message'] + '\n')
        message.close()
        print(f'[X] received {dic}')
        send_email(dic)

    if dic['type_message'] == 'warning' or dic['type_message'] == 'error':
        message = open('/home/christianz/PycharmProjects/RabbitMQ/warning.txt', 'a+')
        message.write(dic['message'] + '\n')
        message.close()
        print(f'[X] received {dic}')
        send_email(dic)

    if dic['type_message'] == 'error':
        message = open('/home/christianz/PycharmProjects/RabbitMQ/error.txt', 'a+')
        message.write(dic['message'] + '\n')
        message.close()
        print(f'[X] received {dic}')
        send_email(dic)


def send_email(dic):
    # create message object instance
    msg = MIMEMultipart()

    message = dic['message']

    # setup the parameters of the message
    password = HideSettings.password
    msg['From'] = HideSettings.email
    msg['To'] = HideSettings.to
    msg['Subject'] = dic['type_message']

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP(HideSettings.smtp, HideSettings.port)
    # smtp.gmail.com 587
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print(f"successfully sent email to: {msg['To']}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)


print('Starting consuming...')
channel.start_consuming()
