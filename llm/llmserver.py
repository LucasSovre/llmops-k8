from redis import Redis as redis
import time
import json
import os

from llama_cpp import Llama
import signal

# Load the Llama model
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "llama-2-7b.Q4_0.gguf")

llm = Llama(
    model_path=MODEL_PATH,
    chat_format="llama-2",
    verbose=False
)

def handle_message(message):
    """Handle messages received from the subscription."""
    decoded_message = message[1].decode('utf-8')
    json_message = json.loads(decoded_message)
    print("begining inference on ticket :", json_message.get("ticket_id"))
    start_ns = time.perf_counter_ns()
    inference = llm(json_message.get("prompt"),
                    max_tokens=int(json_message.get("max_tokens",500)),
                    stop=["Q:", "\n"]
                    )
    end_ns = time.perf_counter_ns()
    print(f"Time taken: {end_ns - start_ns} ns")
    redis_client.publish(json_message.get("ticket_id"), inference["choices"][0]["text"])

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
    message = redis_client.blpop(f"input_queue_{os.getenv('MODEL_NAME','llm_llama')}", timeout=10)
    if message is not None:
        handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)