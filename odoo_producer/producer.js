const amqp = require('amqplib');

// Configuration for the RabbitMQ connection
const rabbitmqHost = 'amqp://user:password@localhost';
const queueName = 'odoo_events';

async function sendMessage() {
  let connection;
  try {
    // 1. Connect to RabbitMQ server
    connection = await amqp.connect(rabbitmqHost);
    console.log('✅ Connected to RabbitMQ');

    // 2. Create a channel
    const channel = await connection.createChannel();
    console.log('✅ Channel created');

    // 3. Assert a queue exists (or create it if it doesn't)
    await channel.assertQueue(queueName, {
      durable: true // The queue will survive a broker restart
    });
    console.log(`✅ Queue '${queueName}' asserted`);

    // 4. Create a sample message representing an Odoo event
    const message = {
      eventId: `evt-${Date.now()}`,
      eventType: 'PRODUCT_UPDATED',
      timestamp: new Date().toISOString(),
      payload: {
        productId: 'PROD-98765',
        name: 'New Product Name',
        price: 199.99
      }
    };
    const messageBuffer = Buffer.from(JSON.stringify(message));

    // 5. Send the message to the queue
    channel.sendToQueue(queueName, messageBuffer, {
      persistent: true // The message will be saved to disk
    });

    console.log(`🚀 Sent message from Odoo to queue '${queueName}':`);
    console.log(JSON.stringify(message, null, 2));

    // 6. Close the channel and connection
    await channel.close();
    await connection.close();
    console.log('✅ Connection closed');

  } catch (error) {
    console.error('❌ Error in Odoo producer:', error);
    if (connection) {
      await connection.close();
      console.log('✅ Connection closed due to error');
    }
    process.exit(1);
  }
}

sendMessage();