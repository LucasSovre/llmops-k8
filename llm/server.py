from redis import Redis as redis
import time
import random
import string
import json

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def handle_message(message):
    """Handle messages received from the subscription."""
    decoded_message = message[1].decode('utf-8')
    json_message = json.loads(decoded_message)
    print("Received message:", json_message)
    # Wait for 2 seconds before publishing a new message
    time_to_wait = random.randint(1, 5)
    for i in range(time_to_wait):
        print(f"Waiting for {time_to_wait} seconds... {i}")
        time.sleep(1)
    # Generate a random string
    random_str = generate_random_string()
    print(f"Publishing random string to output_channel: {random_str}")
    # Publish the random string to another channel
    redis_client.publish(json_message.get("ticket_id"), random_str)

# Connect to Redis
redis_client = redis(host='localhost', port=6379, db=0)

while True:
    # Check for message
    print("Waiting for message from input_queue...")
    message = redis_client.blpop("input_queue", timeout=0)
    print(f"Received message from input_queue: {message}")
    handle_message(message)
    # Sleep to avoid busy-waiting
    time.sleep(0.01)
