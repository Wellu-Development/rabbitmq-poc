require("dotenv").config({ path: "../.env" });
const amqp = require("amqplib");

// Configuration for the RabbitMQ connection
const rabbitmqHost = "amqp://user:password@localhost";
const QUEUE_NAME = process.env.QUEUE_NAME;

async function startConsumer() {
  let connection;
  try {
    // 1. Connect to RabbitMQ server
    connection = await amqp.connect(rabbitmqHost);
    console.log("✅ Connected to RabbitMQ");

    // 2. Create a channel
    const channel = await connection.createChannel();
    console.log("✅ Channel created");

    // 3. Assert the queue exists
    await channel.assertQueue(QUEUE_NAME, {
      durable: true,
    });
    console.log(
      `👂 Waiting for messages in queue '${QUEUE_NAME}'. To exit press CTRL+C`
    );

    // 4. Start consuming messages from the queue
    channel.consume(
      QUEUE_NAME,
      (message) => {
        if (message !== null) {
          try {
            // Process the message
            const messageContent = JSON.parse(message.content.toString());
            console.log(`📥 Received message:`);
            console.log(JSON.stringify(messageContent, null, 2));

            // Here you would have the logic to process the event in SOINDI.
            // For this POC, we'll just simulate it with a log.
            console.log(
              `[SOINDI System] Processing event '${messageContent.eventType}'...`
            );
            console.log(
              `[SOINDI System] Product '${messageContent.payload.name}' data synced.`
            );

            // 5. Acknowledge the message to remove it from the queue
            channel.ack(message);
            console.log("✅ Message acknowledged");
          } catch (e) {
            console.error("❌ Error processing message:", e);
            // 5b. Reject the message if processing fails.
            // 'false' means the message will not be requeued.
            channel.nack(message, false, false);
            console.log("❌ Message rejected (nacked)");
          }
        }
      },
      {
        // Manual acknowledgment mode.
        noAck: false,
      }
    );
  } catch (error) {
    console.error("❌ Error in SOINDI consumer:", error);
    if (connection) {
      await connection.close();
      console.log("✅ Connection closed due to error");
    }
    process.exit(1);
  }
}

startConsumer();
