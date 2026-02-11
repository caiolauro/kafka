# Kafka Learning Repository 🚀

A hands-on repository for learning Apache Kafka fundamentals through practical examples and visual demonstrations.

## Projects

### 📚 [kafka_course_1](./kafka_course_1/)

Introduction to Kafka based on the [Kafka Crash Course](https://www.youtube.com/watch?v=B7CwU_tNYIE). Covers the fundamentals:

- Setting up Kafka locally with Docker (KRaft mode)
- Creating a producer to send messages
- Creating a consumer to receive messages
- Using Kafka CLI tools

### 🎨 [kafka_and_streamlit](./kafka_and_streamlit/)

A visual Streamlit application that demonstrates Kafka's producer-broker-consumer flow in real-time.

![Kafka Flow Visualizer](./kafka_and_streamlit/kafka_workflow_viz.png)

**Features:**
- Interactive order form to produce messages
- Live broker status and topic metadata
- Batch message consumption with full details
- Beautiful dark-themed UI with flow visualization

## Prerequisites

- **Docker** - For running Kafka broker
- **Python 3.11+** - For running producers, consumers, and Streamlit app
- **pip** - For installing dependencies

## Quick Start

```bash
# Clone the repo
cd kafka

# Start with the course fundamentals
cd kafka_course_1
docker-compose up -d
pip install confluent-kafka
python producer.py
python tracker.py

# Or jump to the visual demo
cd ../kafka_and_streamlit
docker-compose up -d
pip install -r requirements.txt
streamlit run app.py
```

## Repository Structure

```
kafka/
├── README.md                 # This file
├── kafka_course_1/           # Kafka fundamentals course
│   ├── docker-compose.yml    # Kafka broker setup
│   ├── producer.py           # CLI message producer
│   ├── tracker.py            # CLI message consumer
│   └── README.md             # Course notes
└── kafka_and_streamlit/      # Visual Streamlit demo
    ├── docker-compose.yml    # Kafka broker setup
    ├── app.py                # Streamlit application
    ├── producer.py           # Standalone producer
    ├── tracker.py            # Standalone consumer
    ├── requirements.txt      # Python dependencies
    └── README.md             # Project documentation
```

## Key Concepts Covered

| Concept | Description |
|---------|-------------|
| **Producer** | Sends messages to Kafka topics |
| **Consumer** | Reads messages from Kafka topics |
| **Broker** | Kafka server that stores and serves messages |
| **Topic** | Category/feed where messages are published |
| **Partition** | Subdivision of a topic for parallelism |
| **Offset** | Position of a message within a partition |
| **Consumer Group** | Group of consumers sharing message consumption |

## Tech Stack

- **Apache Kafka** (Confluent) - Message streaming platform
- **Docker** - Containerization
- **Python** - Application code
- **confluent-kafka** - Python Kafka client
- **Streamlit** - Web UI framework

## License

MIT
