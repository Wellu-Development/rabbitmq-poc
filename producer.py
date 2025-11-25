import os
import json
import random
import string
import time
import pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
QUEUE_NAME = os.getenv("QUEUE_NAME", "odoo-events")


def get_connection():
    if not RABBITMQ_HOST:
        raise ValueError("RABBITMQ_HOST environment variable is not set")

    if RABBITMQ_HOST.startswith("amqp"):
        params = pika.URLParameters(RABBITMQ_HOST)
    else:
        params = pika.ConnectionParameters(host=RABBITMQ_HOST)

    return pika.BlockingConnection(params)


def generate_random_data():
    default_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    quantity = random.randint(1, 100)

    return {"default_code": default_code, "quantity": quantity}


def main():
    connection = None
    try:
        connection = get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        print(f" [*] Connected to RabbitMQ. Sending messages to '{QUEUE_NAME}'...")
        print(" [*] Press CTRL+C to exit")

        while True:
            data = generate_random_data()
            message = json.dumps(data)

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            print(f" [x] Sent {message}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()


if __name__ == "__main__":
    main()
