import pika
import json
import sys

def main():
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    # Declare a durable queue
    queue_name = 'python_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    # Create a message
    message = {
        'source': 'Python Producer',
        'payload': 'This is the the Python message.'
    }
    body = json.dumps(message)

    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(f" [🚀] Sent {message}")

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
