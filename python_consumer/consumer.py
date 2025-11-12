import pika
import json
import sys
import time
import os
from dotenv import load_dotenv

    # Load environment variables from .env file
load_dotenv()

QUEUE_NAME = os.getenv('QUEUE_NAME')


def main():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    # Declare the queue to ensure it exists
    # queue_name = 'python_queue'
    queue_name = QUEUE_NAME
    channel.queue_declare(queue=queue_name, durable=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] Received {json.loads(body)}")
        # Simulate work
        time.sleep(1)
        print(" [x] Done")
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up subscription on the queue
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

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
