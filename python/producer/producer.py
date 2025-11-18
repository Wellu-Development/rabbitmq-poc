import pika
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file. This is crucial for configuring
# RabbitMQ connection details and the queue name without hardcoding them,
# making the application more flexible and secure.
load_dotenv()

# Retrieve the queue name from environment variables. This queue will be used
# for sending messages to RabbitMQ.
QUEUE_NAME = os.getenv('QUEUE_NAME')

# Retrieve RabbitMQ user and password from environment variables,
# with default values for convenience during development.
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

    # Declare a durable queue. 'durable=True' ensures that the queue
    # survives a RabbitMQ broker restart. Messages will not be lost if the broker goes down.
    channel.queue_declare(queue=queue_name, durable=True)

    # Construct the message payload.
    # The 'source' indicates where the message originated, and 'payload' contains
    # the actual data, which can be provided via command-line arguments or a default string.
    message = {
        'source': 'Python Producer',
        'payload': " ".join(sys.argv[1::]) or 'This is the the Python message.'
    }
    # Convert the message dictionary to a JSON string, as RabbitMQ messages are typically
    # sent as strings or byte arrays.
    body = json.dumps(message)

    # Publish the message to the queue.
    # - `exchange=''` uses the default exchange.
    # - `routing_key=queue_name` directs the message to our declared queue.
    # - `body=body` is the message content.
    # - `properties=pika.BasicProperties(delivery_mode=2)` makes the message persistent,
    #   meaning it will be written to disk and survive a broker restart.
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(f" [🚀] Sent {message}")

    # Close the connection to RabbitMQ. It's good practice to close connections
    # when they are no longer needed to free up resources.
    connection.close()

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
