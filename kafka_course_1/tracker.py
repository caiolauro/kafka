# first connect to a kafka broker


from confluent_kafka import Consumer
import json

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "tracker",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_config)

consumer.subscribe(["orders"])

print("🟢 Consumer is running and subscribed to orders topic")
try:
    while True:
        message = consumer.poll(1.0)  # 1.0 means wait for 1 second for a message
        if message is None:
            continue
        if message.error():
            print(f"🔴 Error: {message.error()}")
            continue
        value = message.value().decode("utf-8")
        order = json.loads(value)
        print(f"🟢 Received message: {order}")
        consumer.commit()
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")
finally:
    consumer.close()
