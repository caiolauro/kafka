"""
Kafka & Streamlit Integration Demo
Visualizes Kafka producer, broker, and consumer interactions.
"""

import streamlit as st
import json
import uuid
from datetime import datetime
from typing import Optional
import threading
import time
from queue import Queue
from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

# ─────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kafka Flow Visualizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS for Beautiful UI
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700&display=swap');
    
    :root {
        --producer-color: #4ade80;
        --broker-color: #fbbf24;
        --consumer-color: #60a5fa;
        --bg-dark: #0a0f1a;
        --bg-card: #141c2e;
        --text-primary: #ffffff;
        --text-secondary: #e2e8f0;
        --text-muted: #cbd5e1;
    }
    
    /* Global app background */
    .stApp {
        background: linear-gradient(160deg, #0a0f1a 0%, #162033 50%, #0d1321 100%);
    }
    
    /* Force all text to be readable */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #e2e8f0 !important;
    }
    
    /* Main header styling */
    .main-header {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4ade80, #fbbf24, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-family: 'IBM Plex Mono', monospace;
        color: #cbd5e1 !important;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* Section title styling */
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Card components */
    .component-card {
        background: linear-gradient(145deg, #1a2744, #243352);
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid #334766;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 1rem;
    }
    
    .producer-card { border-left: 4px solid #4ade80; }
    .broker-card { border-left: 4px solid #fbbf24; }
    .consumer-card { border-left: 4px solid #60a5fa; }
    
    .card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .producer-title { color: #4ade80 !important; }
    .broker-title { color: #fbbf24 !important; }
    .consumer-title { color: #60a5fa !important; }
    
    /* Form labels - HIGH VISIBILITY */
    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label,
    .stForm label,
    [data-testid="stWidgetLabel"] {
        color: #f1f5f9 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Form inputs */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox > div > div {
        background: #0f1729 !important;
        border: 1px solid #3d4f6f !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #4ade80 !important;
        box-shadow: 0 0 0 2px rgba(74, 222, 128, 0.2) !important;
    }
    
    /* Selectbox dropdown */
    .stSelectbox [data-baseweb="select"] {
        background: #0f1729 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: #0f1729 !important;
        border: 1px solid #3d4f6f !important;
        color: #ffffff !important;
    }
    
    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown strong {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #1a2744 !important;
        border: 1px solid #334766 !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    .streamlit-expanderContent {
        background: #0f1729 !important;
        border: 1px solid #334766 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* JSON display */
    .stJson {
        background: #0a0f1a !important;
        border-radius: 8px !important;
    }
    
    /* Captions */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4ade80, #22c55e) !important;
        color: #0a0f1a !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(74, 222, 128, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(74, 222, 128, 0.5) !important;
    }
    
    .stButton > button:disabled {
        background: #334766 !important;
        color: #64748b !important;
        box-shadow: none !important;
    }
    
    /* Form submit button */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #4ade80, #22c55e) !important;
        color: #0a0f1a !important;
        font-weight: 700 !important;
    }
    
    /* Success/Error/Info messages */
    .stSuccess {
        background: rgba(74, 222, 128, 0.15) !important;
        border: 1px solid #4ade80 !important;
        color: #bbf7d0 !important;
    }
    
    .stError {
        background: rgba(248, 113, 113, 0.15) !important;
        border: 1px solid #f87171 !important;
        color: #fecaca !important;
    }
    
    .stInfo {
        background: rgba(96, 165, 250, 0.15) !important;
        border: 1px solid #60a5fa !important;
        color: #bfdbfe !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.15) !important;
        border: 1px solid #fbbf24 !important;
        color: #fef08a !important;
    }
    
    /* Flow arrow animation */
    .flow-arrow {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.5rem;
        color: #fbbf24;
        animation: pulse 2s infinite;
        text-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.15); }
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1729, #162033) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    
    /* Code blocks */
    .stCode, code {
        background: #0a0f1a !important;
        color: #4ade80 !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    
    /* Dividers */
    hr {
        border-color: #334766 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4ade80 transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Kafka Configuration
# ─────────────────────────────────────────────────────────────────────────────
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "orders"

# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────────────────────────────────────
if "produced_messages" not in st.session_state:
    st.session_state.produced_messages = []
if "consumed_messages" not in st.session_state:
    st.session_state.consumed_messages = []
if "kafka_connected" not in st.session_state:
    st.session_state.kafka_connected = False
if "message_queue" not in st.session_state:
    st.session_state.message_queue = Queue()
if "consumer_running" not in st.session_state:
    st.session_state.consumer_running = False


# ─────────────────────────────────────────────────────────────────────────────
# Kafka Helper Functions
# ─────────────────────────────────────────────────────────────────────────────
def check_kafka_connection() -> bool:
    """Check if Kafka broker is reachable."""
    try:
        admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
        metadata = admin.list_topics(timeout=5)
        return True
    except Exception as e:
        return False


def ensure_topic_exists():
    """Create the orders topic if it doesn't exist."""
    try:
        admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
        topics = admin.list_topics(timeout=5).topics
        if TOPIC_NAME not in topics:
            new_topic = NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)
            admin.create_topics([new_topic])
            time.sleep(1)  # Wait for topic creation
    except Exception as e:
        st.error(f"Failed to ensure topic exists: {e}")


def create_producer() -> Optional[Producer]:
    """Create a Kafka producer."""
    try:
        return Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    except Exception as e:
        st.error(f"Failed to create producer: {e}")
        return None


def produce_message(producer: Producer, order: dict) -> dict:
    """Produce a message to Kafka and return delivery info."""
    delivery_info = {"success": False, "error": None, "details": {}}
    
    def delivery_callback(err, msg):
        if err:
            delivery_info["error"] = str(err)
        else:
            delivery_info["success"] = True
            delivery_info["details"] = {
                "topic": msg.topic(),
                "partition": msg.partition(),
                "offset": msg.offset(),
                "timestamp": msg.timestamp()[1] if msg.timestamp() else None,
            }
    
    value = json.dumps(order).encode("utf-8")
    producer.produce(
        topic=TOPIC_NAME,
        value=value,
        callback=delivery_callback,
    )
    producer.flush(timeout=5)
    return delivery_info


def consume_messages_batch(max_messages: int = 10, timeout: float = 2.0) -> list:
    """Consume a batch of messages from Kafka."""
    messages = []
    try:
        consumer = Consumer({
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": f"streamlit-consumer-{uuid.uuid4().hex[:8]}",
            "auto.offset.reset": "latest",
        })
        consumer.subscribe([TOPIC_NAME])
        
        while True:
            msg = consumer.poll(1)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    break
                continue
            
            value = json.loads(msg.value().decode("utf-8"))
            messages.append({
                "data": value,
                "partition": msg.partition(),
                "offset": msg.offset(),
                "timestamp": msg.timestamp()[1] if msg.timestamp() else None,
            })
            st.write(f"🟢 Received message: {value}")
        
        consumer.close()
    except Exception as e:
        st.error(f"Consumer error: {e}")
    
    return messages


# ─────────────────────────────────────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">🚀 Kafka Flow Visualizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">PRODUCER ➜ BROKER ➜ CONSUMER &nbsp;│&nbsp; Real-time Message Flow</p>', unsafe_allow_html=True)


def render_connection_status():
    """Render Kafka connection status."""
    connected = check_kafka_connection()
    st.session_state.kafka_connected = connected
    
    if connected:
        st.success("✅ Connected to Kafka broker at `localhost:9092`")
        ensure_topic_exists()
    else:
        st.error("❌ Cannot connect to Kafka broker. Make sure Docker is running: `docker-compose up -d`")
    
    return connected


def render_producer_section():
    """Render the producer section with order form."""
    st.markdown("""
    <div class="component-card producer-card">
        <div class="card-title producer-title">📤 PRODUCER</div>
        <p style="color: #a1a1aa; font-size: 0.85rem; margin-top: -0.5rem;">Send orders to Kafka topic</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            user = st.text_input("👤 Customer Name", value="Marcia")
            item = st.selectbox("🍽️ Item", [
                "Spaghetti Carbonara",
                "Margherita Pizza",
                "Caesar Salad",
                "Grilled Salmon",
                "Beef Stroganoff",
            ])
        
        with col2:
            quantity = st.number_input("📦 Quantity", min_value=1, max_value=10, value=2)
            total = st.number_input("💰 Total ($)", min_value=1.0, max_value=500.0, value=25.00, step=0.50)
        
        submitted = st.form_submit_button("🚀 Produce Message", use_container_width=True)
        
        if submitted and st.session_state.kafka_connected:
            order = {
                "order_id": str(uuid.uuid4()),
                "user": user,
                "item": item,
                "quantity": quantity,
                "total": total,
                "status": "pending",
                "timestamp": datetime.now().isoformat(),
            }
            
            producer = create_producer()
            if producer:
                result = produce_message(producer, order)
                if result["success"]:
                    st.session_state.produced_messages.append({
                        "order": order,
                        "delivery": result["details"],
                    })
                    st.success(f"✅ Message delivered to partition {result['details']['partition']} at offset {result['details']['offset']}")
                else:
                    st.error(f"❌ Failed to deliver message: {result['error']}")
    
    # Show produced messages
    if st.session_state.produced_messages:
        st.markdown("**📋 Produced Messages:**")
        for i, msg in enumerate(reversed(st.session_state.produced_messages[-5:])):
            with st.expander(f"Order: {msg['order']['order_id'][:8]}... | {msg['order']['item']}", expanded=(i == 0)):
                st.json(msg["order"])
                st.caption(f"Partition: {msg['delivery']['partition']} | Offset: {msg['delivery']['offset']}")


def render_broker_section():
    """Render the broker visualization section."""
    st.markdown("""
    <div class="component-card broker-card">
        <div class="card-title broker-title">🏢 KAFKA BROKER</div>
        <p style="color: #a1a1aa; font-size: 0.85rem; margin-top: -0.5rem;">Topic & partition status</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.kafka_connected:
        try:
            admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
            metadata = admin.list_topics(timeout=5)
            
            # Show topic info
            if TOPIC_NAME in metadata.topics:
                topic_meta = metadata.topics[TOPIC_NAME]
                partitions = len(topic_meta.partitions)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Topic", TOPIC_NAME)
                with col2:
                    st.metric("Partitions", partitions)
                with col3:
                    st.metric("Status", "🟢 Active")
                
                # Visual representation
                st.markdown("**📊 Topic Partitions:**")
                for pid, pinfo in topic_meta.partitions.items():
                    st.markdown(f"- Partition `{pid}` → Leader: `{pinfo.leader}`")
            else:
                st.info(f"Topic `{TOPIC_NAME}` will be created when you produce the first message.")
        except Exception as e:
            st.error(f"Error fetching broker info: {e}")
    else:
        st.warning("Connect to Kafka to see broker details")


def render_consumer_section():
    """Render the consumer section."""
    st.markdown("""
    <div class="component-card consumer-card">
        <div class="card-title consumer-title">📥 CONSUMER</div>
        <p style="color: #a1a1aa; font-size: 0.85rem; margin-top: -0.5rem;">Receive messages from topic</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔄 Consume Messages", use_container_width=True, disabled=not st.session_state.kafka_connected):
            with st.spinner("Consuming messages..."):
                messages = consume_messages_batch(max_messages=20, timeout=3.0)
                if messages:
                    st.session_state.consumed_messages.extend(messages)
                    st.success(f"✅ Consumed {len(messages)} message(s)")
                else:
                    st.info("No new messages available")
    
    with col2:
        if st.button("🗑️ Clear Consumed", use_container_width=True):
            st.session_state.consumed_messages = []
            st.rerun()
    
    # Show consumed messages
    if st.session_state.consumed_messages:
        st.markdown(f"**📋 Consumed Messages ({len(st.session_state.consumed_messages)}):**")
        for i, msg in enumerate(reversed(st.session_state.consumed_messages[-10:])):
            order = msg["data"]
            with st.expander(f"🛒 {order.get('user', 'Unknown')} | {order.get('item', 'N/A')} | ${order.get('total', 0):.2f}", expanded=(i == 0)):
                st.json(order)
                st.caption(f"Partition: {msg['partition']} | Offset: {msg['offset']}")
    else:
        st.info("No messages consumed yet. Click 'Consume Messages' to fetch from Kafka.")


def render_flow_diagram():
    """Render a visual flow diagram."""
    st.markdown("---")
    st.markdown("### 🔄 Message Flow Visualization")
    
    cols = st.columns([1, 0.3, 1, 0.3, 1])
    
    with cols[0]:
        produced_count = len(st.session_state.produced_messages)
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 1rem; background: linear-gradient(145deg, rgba(74,222,128,0.15), rgba(34,197,94,0.05)); border-radius: 16px; border: 2px solid #4ade80; box-shadow: 0 0 30px rgba(74,222,128,0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📤</div>
            <div style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #4ade80; font-size: 1.1rem; letter-spacing: 0.1em;">PRODUCER</div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">{produced_count}</div>
            <div style="color: #a1a1aa; font-size: 0.85rem; font-family: 'Outfit', sans-serif;">messages sent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown('<div class="flow-arrow">➜</div>', unsafe_allow_html=True)
    
    with cols[2]:
        status = "🟢" if st.session_state.kafka_connected else "🔴"
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 1rem; background: linear-gradient(145deg, rgba(251,191,36,0.15), rgba(245,158,11,0.05)); border-radius: 16px; border: 2px solid #fbbf24; box-shadow: 0 0 30px rgba(251,191,36,0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏢</div>
            <div style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #fbbf24; font-size: 1.1rem; letter-spacing: 0.1em;">BROKER</div>
            <div style="font-size: 2.2rem; margin: 0.5rem 0;">{status}</div>
            <div style="color: #a1a1aa; font-size: 0.85rem; font-family: 'IBM Plex Mono', monospace;">localhost:9092</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown('<div class="flow-arrow">➜</div>', unsafe_allow_html=True)
    
    with cols[4]:
        consumed_count = len(st.session_state.consumed_messages)
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 1rem; background: linear-gradient(145deg, rgba(96,165,250,0.15), rgba(59,130,246,0.05)); border-radius: 16px; border: 2px solid #60a5fa; box-shadow: 0 0 30px rgba(96,165,250,0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📥</div>
            <div style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #60a5fa; font-size: 1.1rem; letter-spacing: 0.1em;">CONSUMER</div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">{consumed_count}</div>
            <div style="color: #a1a1aa; font-size: 0.85rem; font-family: 'Outfit', sans-serif;">messages received</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
def main():
    render_header()
    
    # Connection status
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        connected = render_connection_status()
        
        st.markdown("---")
        st.markdown("### 📊 Session Stats")
        st.metric("Produced", len(st.session_state.produced_messages))
        st.metric("Consumed", len(st.session_state.consumed_messages))
        
        st.markdown("---")
        if st.button("🗑️ Reset Session", use_container_width=True):
            st.session_state.produced_messages = []
            st.session_state.consumed_messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📖 Quick Start")
        st.code("docker-compose up -d", language="bash")
        st.caption("Start Kafka broker first, then use the UI to produce and consume messages.")
    
    # Flow diagram
    render_flow_diagram()
    
    st.markdown("---")
    
    # Main columns for producer and consumer
    col1, col2, col3 = st.columns([1, 0.8, 1])
    
    with col1:
        render_producer_section()
    
    with col2:
        render_broker_section()
    
    with col3:
        render_consumer_section()


if __name__ == "__main__":
    main()
