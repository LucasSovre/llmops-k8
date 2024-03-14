from redis import Redis as redis
import time
import json
import os

from sentence_transformers import SentenceTransformer
import signal

# Load the Llama model
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "e5-large-v2")

model = SentenceTransformer(MODEL_PATH)

def handle_message(message):
    """Handle messages received from the subscription."""
    decoded_message = message[1].decode('utf-8')
    json_message = json.loads(decoded_message)
    print("begining inference on ticket :", json_message.get("ticket_id"))
    start_ns = time.perf_counter_ns()
    embeddings = model.encode(json.loads(json_message.get("prompt")), normalize_embeddings=True)
    scores = (embeddings[:2] @ embeddings[2:].T) * 100
    end_ns = time.perf_counter_ns()
    print(f"Time taken: {end_ns - start_ns} ns")
    redis_client.publish(json_message.get("ticket_id"), json.dumps(scores.tolist()))

# Connect to Redis
redis_client = redis(host='localhost', port=6379, db=0)

# Define a flag to control the loop
running = True

def stop_running(signum, frame):
    """Handle signal by setting the running flag to False."""
    print("Received stop signal, stopping...")
    global running
    running = False

# Register the signal handler
signal.signal(signal.SIGINT, stop_running)
signal.signal(signal.SIGTERM, stop_running)

print("Waiting for message from input_queue...")

while running:
    # Check for message
    message = redis_client.blpop(f"input_queue_{os.getenv('MODEL_NAME','embeding_e5')}", timeout=10)
    if message is not None:
        handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)