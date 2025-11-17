import pika
import json
import sys
import time
import os
from dotenv import load_dotenv

    # Load environment variables from .env file
load_dotenv()

QUEUE_NAME = os.getenv('QUEUE_NAME')


RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')

def main():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    # Declare a fanout exchange
    exchange_name = 'logs'
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    # Declare a non-durable, exclusive queue with a random name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    print(f" [*] Waiting for logs in '{queue_name}'. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] {body.decode()}")

    # Set up subscription on the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
