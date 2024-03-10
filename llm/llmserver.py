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
    json_message = message['data'].decode('utf-8')
    json_message = json.loads(json_message)
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
pubsub = redis_client.pubsub()

# Subscribe to the input_channel
pubsub.subscribe(**{'input_channel': handle_message})

print("Subscribed to 'input_channel'. Waiting for messages...")

while True:
    # Check for message
    message = pubsub.get_message()
    if message and message['type'] == 'message':
        handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)