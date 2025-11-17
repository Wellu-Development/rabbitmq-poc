from multiprocessing import process
import queue
import pika
import json
import sys
import os
from dotenv import load_dotenv

    # Load environment variables from .env file
load_dotenv()

QUEUE_NAME = os.getenv('QUEUE_NAME')

RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')

import random

def main():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    # Declare a stream
    stream_name = 'inventory_updates'
    channel.queue_declare(queue=stream_name, durable=True, arguments={'x-queue-type': 'stream'})

    # Publish a large number of messages
    num_messages = 100000
    print(f" [🚀] Sending {num_messages} messages...")

    for i in range(num_messages):
        sku = f"SKU-{random.randint(1, 1000)}"
        change = random.randint(-10, 10)
        sign = '+' if change >= 0 else ''
        message = f"{sku}, {sign}{change}"
        body = message

        channel.basic_publish(
            exchange='',
            routing_key=stream_name,
            body=body)

    print(f" [🚀] Sent {num_messages} messages to stream '{stream_name}'")

    # Close the connection
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
