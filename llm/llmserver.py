from redis import Redis as redis
import time
import json
import os

from llama_cpp import Llama

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
    print("beging inference on ticket :", json_message.get("ticket_id"))
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

while True:
    # Check for message
    print("Waiting for message from input_queue...")
    message = redis_client.blpop("input_queue", timeout=0)
    print(f"Received message from input_queue:")
    handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)