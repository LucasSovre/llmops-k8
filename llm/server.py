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
    json_message = message['data'].decode('utf-8')
    json_message = json.loads(json_message)
    print("Received message:", json_message)
    # Wait for 2 seconds before publishing a new message
    for i in range(3):
        print(f"Waiting for 3 seconds... {i}")
        time.sleep(1)
    # Generate a random string
    random_str = generate_random_string()
    print(f"Publishing random string to output_channel: {random_str}")
    # Publish the random string to another channel
    redis_client.publish(json_message.get("ticket_id"), random_str)

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
