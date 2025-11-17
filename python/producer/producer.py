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

def main():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    # Declare a durable queue
    queue_name = 'task_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    # Create a message
    message = ' '.join(sys.argv[1::]) or "Hello World!"
    body = message

    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(f" [🚀] Sent '{message}'")

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
