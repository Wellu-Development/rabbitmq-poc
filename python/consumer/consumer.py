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

    # Declare the stream to ensure it exists
    stream_name = 'inventory_updates'
    channel.queue_declare(queue=stream_name, durable=True, arguments={'x-queue-type': 'stream'})
    
    channel.basic_qos(prefetch_count=1) 

    offset = sys.argv[1] if len(sys.argv) > 1 else 'next'

    print(f" [*] Waiting for messages in stream '{stream_name}' with offset '{offset}'. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    # Set up subscription on the stream
    channel.basic_consume(
        queue=stream_name,
        on_message_callback=callback,
        auto_ack=False,
        arguments={'x-stream-offset': offset}
    )

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
