from redis import Redis as redis
import time
import json
import os
import logging

from llama_cpp import Llama
import signal

# Load the Llama model
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "llama-2-7b.Q4_0.gguf")

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    handlers=[logging.StreamHandler()],
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Loading model...")
llm = Llama(
    model_path=MODEL_PATH,
    chat_format="llama-2",
    verbose=False
)
logging.info("model loaded")

def handle_message(message):
    """Handle messages received from the subscription."""
    decoded_message = message[1].decode('utf-8')
    json_message = json.loads(decoded_message)
    logging.debug(f"Received message: {decoded_message}")
    logging.debug(f"Prompt: {json_message.get('prompt')}")
    logging.info("Starting inference on ticket: %s", json_message.get("ticket_id"))
    start_ns = time.perf_counter_ns()
    inference = llm(json_message.get("prompt"),
                    max_tokens=int(json_message.get("max_tokens",500)),
                    stop=["Q:", "\n"]
                    )
    end_ns = time.perf_counter_ns()
    logging.info("Inference on ticket %s took %s s", json_message.get("ticket_id"), (end_ns - start_ns) / 1e9)
    redis_client.publish(json_message.get("ticket_id"), json.dumps({
        "result" : inference["choices"][0]["text"],
        "process_time": (end_ns - start_ns) / 1e9
        }))

# Connect to Redis
redis_client = redis(host=os.getenv("REDIS_HOST",'localhost'), port=6379, db=0)

# Define a flag to control the loop
running = True

def stop_running(signum, frame):
    """Handle signal by setting the running flag to False."""
    logging.info("Received signal %s, stopping the server...", signum)
    global running
    running = False

# Register the signal handler
signal.signal(signal.SIGINT, stop_running)
signal.signal(signal.SIGTERM, stop_running)

logging.info("Starting the server...")

while running:
    logging.debug("Checking for messages...")
    # Check for message
    message = redis_client.blpop(f"input_queue_{os.getenv('MODEL_NAME','llm_llama')}", timeout=10)
    if message is not None:
        handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)