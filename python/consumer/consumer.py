import pika
import json
import sys
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file. This ensures that configuration
# details like the queue name and RabbitMQ credentials are not hardcoded,
# promoting flexibility and security.
load_dotenv()

# Retrieve the queue name from environment variables. This is the queue
# from which the consumer will receive messages.
QUEUE_NAME = os.getenv('QUEUE_NAME')

# Retrieve RabbitMQ user and password from environment variables,
# providing default values for development convenience.
RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')

def main():
    # Establish a connection to the RabbitMQ server.
    # It uses credentials for authentication and connects to 'localhost'.
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    
    # Create a channel, which is where most of the API for getting things done resides.
    channel = connection.channel()

    # Declare the queue to ensure it exists. This is important because the consumer
    # needs to be sure the queue it's trying to consume from is present.
    # 'durable=True' ensures the queue survives a broker restart.
    channel.queue_declare(queue=queue_name, durable=True)

    print(' [*] Waiting for messages in \"%s\". To exit press CTRL+C' % QUEUE_NAME)

    # Define the callback function that will be executed when a message is received.
    def callback(ch, method, properties, body):
        # Decode and print the received message body.
        print(f" [x] Received {json.loads(body)}")
        # Simulate work being done by the consumer. This helps demonstrate
        # message processing time and how acknowledgements work.
        time.sleep(1)
        print(" [x] Done")
        # Acknowledge the message. This tells RabbitMQ that the message has been
        # successfully processed and can be removed from the queue.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up Quality of Service (QoS) with prefetch_count=1.
    # This tells RabbitMQ not to give more than one message to a worker at a time.
    # Or, in other words, don't dispatch a new message to a worker until it has
    # processed and acknowledged the previous one.
    channel.basic_qos(prefetch_count=1)
    
    # Set up the consumer to listen for messages on the specified queue and
    # execute the 'callback' function when a message arrives.
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    # Start consuming messages. This enters a blocking loop that waits for data,
    # runs callbacks, and handles network heartbeats.
    channel.start_consuming()

if __name__ == '__main__':
    # Entry point for the script.
    try:
        main()
    except KeyboardInterrupt:
        # Handle graceful exit on Ctrl+C.
        print('Interrupted')
        sys.exit(0)
    except Exception as e:
        # Catch and report any other exceptions that occur during execution.
        print(f"An error occurred: {e}")
        sys.exit(1)
