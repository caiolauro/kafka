from confluent_kafka import Producer
from datetime import datetime
import json
import uuid


producer_config = {"bootstrap.servers": "localhost:9092"}
producer = Producer(producer_config)


def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Delivered to topic {msg.value().decode('utf-8')}")
        print(
            f"Delivered to topic {msg.topic()} : partition {msg.partition()}: at offset {msg.offset()}"
        )
        print(f"Delivered to timestamp {msg.timestamp()}")
        print(f"Delivered to key {msg.key()}")
        print(f"Delivered to value {msg.value()}")
        print(f"Delivered to headers {msg.headers()}")
        print(f"Delivered to timestamp {msg.timestamp()}")


order = {
    "order_id": str(uuid.uuid4()),
    "user": "Marcia",
    "item": "Spaghetti Carbonara",
    "quantity": 2,
    "total": 25.00,
    "status": "pending",
    "timestamp": datetime.now().isoformat(),
}

value = json.dumps(order).encode("utf-8")

# Please send the message to the topic "orders"
producer.produce(
    topic="orders",
    value=value,
    callback=delivery_report,
)
producer.flush()  # Best practice: flushing makes sure the buffered messages are sent to the broker
