# RabbitMQ Producer-Consumer POC: Odoo to SOINDI Integration

This Proof of Concept (POC) demonstrates how to use RabbitMQ as a message broker to decouple a new system (Odoo) from a legacy system (SOINDI). It follows a simple **Producer-Consumer** pattern.

-   **Node.js Producer (`odoo_producer/`)**: A Node.js script that simulates the Odoo system publishing an event (e.g., "Product Updated") to a RabbitMQ queue.
-   **Node.js Consumer (`soindi_consumer/`)**: A Node.js script that simulates the SOINDI legacy system listening for events from the queue and processing them (e.g., to keep its own data in sync).

## Additional Python Examples

For demonstration purposes, two more producer-consumer pairs have been added, implemented in Python. These demonstrate the language-agnostic nature of RabbitMQ.

-   **Python Producer 1 (`python_producer_1/`)**: Sends a message to `python_queue_1`.
-   **Python Consumer 1 (`python_consumer_1/`)**: Consumes messages from `python_queue_1`.
-   **Python Producer 2 (`python_producer_2/`)**: Sends a message to `python_queue_2`.
-   **Python Consumer 2 (`python_consumer_2/`)**: Consumes messages from `python_queue_2`.

## The Power of Decoupling

This architecture brings to light the critical advantage of decoupling:

**Odoo (the producer) does not need to know anything about SOINDI (the consumer).**

-   **No Direct Connection**: Odoo's only job is to send a message to a specific RabbitMQ queue. It has no awareness of which system will pick it up, where that system is, or even if it's currently online. This is crucial for allowing the legacy system to process data on its own terms without slowing down the modern system.
-   **Resilience**: If the SOINDI consumer is offline for maintenance or due to a crash, the messages from Odoo will safely persist in the RabbitMQ queue. Once SOINDI comes back online, it can immediately start processing the backlog of messages. The systems don't have to be available at the same time.
-   **Scalability**: If the volume of events from Odoo increases, we can potentially scale the processing power by running multiple instances of the SOINDI consumer (if the legacy system supports it).
-   **Flexibility**: If a new system (e.g., a data warehouse) needs to be notified of the same "Product Updated" event, we can add another consumer to listen to the same messages without making any changes to Odoo.

This message queue acts as a "glue" or middleware that allows two independent systems to communicate asynchronously and reliably.

## How to Run the POC

### Prerequisites

-   Docker and Docker Compose
-   Node.js and npm
-   Python 3 and pip

### 1. Start RabbitMQ Server

Open a terminal and run the following command from the root of the project:

```bash
docker-compose up -d
```

This will start a RabbitMQ container in the background.

-   You can access the RabbitMQ Management UI at [http://localhost:15672](http://localhost:15672).
-   Use the credentials `user` / `password` to log in.

### 2. Run the Node.js Consumer (SOINDI)

Open a **new terminal** and navigate to the `soindi_consumer` directory. Install dependencies and start the listener:

```bash
cd soindi_consumer
npm install
npm start
```

The consumer will connect to RabbitMQ and wait for messages on the `odoo_events` queue.

### 3. Run the Node.js Producer (Odoo)

Open a **third terminal** and navigate to the `odoo_producer` directory. Install dependencies and run the script to send a message:

```bash
cd odoo_producer
npm install
npm start
```

### 4. Run the Python Examples

For each Python producer/consumer pair, you'll need two separate terminals.

**For Python Producer 1 and Consumer 1:**

**Consumer 1:**
Open a new terminal:
```bash
cd python_consumer_1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py
```

**Producer 1:**
Open another new terminal:
```bash
cd python_producer_1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 producer.py
```

**For Python Producer 2 and Consumer 2:**

**Consumer 2:**
Open a new terminal:
```bash
cd python_consumer_2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py
```

**Producer 2:**
Open another new terminal:
```bash
cd python_producer_2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 producer.py
```

### Expected Outcome

1.  The **Odoo producer terminal** will show a confirmation that it connected and sent a message.
2.  The **SOINDI consumer terminal** will show that it received the message and is "processing" it.
3.  Similarly, each Python producer will send a message, and its corresponding Python consumer will receive and print it.
4.  If you check the RabbitMQ Management UI, you will see the `odoo_events`, `python_queue_1`, and `python_queue_2` queues and can observe the message flow.

This completes the demonstration of a decoupled workflow using RabbitMQ with examples in both Node.js and Python.
