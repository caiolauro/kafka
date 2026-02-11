# Kafka Flow Visualizer 🚀

Integrate the first kafka course demo to Streamlit UI to demonstrate producer, broker and consumer visually.

![Kafka Flow Visualizer](kafka_workflow_viz.png)

## Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KAFKA FLOW VISUALIZER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────┐           ┌──────────┐           ┌──────────┐              │
│    │          │    ──►    │          │    ──►    │          │              │
│    │ PRODUCER │           │  BROKER  │           │ CONSUMER │              │
│    │          │           │          │           │          │              │
│    └──────────┘           └──────────┘           └──────────┘              │
│         │                      │                      │                     │
│    Order Form              Topic Info            Message List               │
│    Send Messages          Partitions             Consume Batch              │
│    Delivery Status        Connection             Real-time View             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architecture

- **Producer Section**: Interactive form to create and send order messages
- **Broker Section**: Live status of Kafka broker, topic metadata, partitions
- **Consumer Section**: Batch consume and display messages from the topic

## Quick Start

### 1. Start Kafka Broker

```bash
docker-compose up -d
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App

```bash
streamlit run app.py
```

### 4. Open Browser

Navigate to http://localhost:8501

## Features

- **Visual Flow Diagram**: See message counts flow through producer → broker → consumer
- **Interactive Producer**: Create orders with custom items, quantities, and prices
- **Broker Monitoring**: View topic partitions and connection status
- **Batch Consumer**: Consume messages on-demand with full metadata display
- **Session Tracking**: Track produced/consumed message counts
- **Modern UI**: Dark theme with gradient backgrounds and smooth animations

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `producer.py` | Standalone CLI producer (original demo) |
| `tracker.py` | Standalone CLI consumer (original demo) |
| `docker-compose.yml` | Kafka broker (KRaft mode) |
| `requirements.txt` | Python dependencies |

## Usage Tips

1. **Start Kafka first** - The app checks for broker connectivity on load
2. **Produce messages** - Use the form to send test orders
3. **Consume messages** - Click "Consume Messages" to batch read from Kafka
4. **Reset session** - Clear counters and start fresh from the sidebar