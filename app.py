import time
import os
import redis
import logging

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


# write to redis instance
def write_random_numbers_to_redis():
    # Retrieves the Redis server host and port from the environment variables set in the manifest file or set default values if they are not provided.
    redis_host = os.environ.get("REDIS_HOST", "redis")
    redis_port_str = os.environ.get("REDIS_PORT", "6379")
    redis_port = int(redis_port_str.split(':')[-1]) if 'tcp://' in redis_port_str else int(redis_port_str)

    # Creates a Redis client instance named cache using the host, port, and database number.
    cache = redis.Redis(host=redis_host, port=redis_port, db=0)

    numb = 0
    while True:
        output_dict = {"temp": 0, "temp2": 1}

        print(output_dict)
        hash_key = 'key-' + str(numb)
        cache.hmset(hash_key, output_dict)

        logging.info(f"Wrote {output_dict} to Redis")
        numb = numb + 1

        time.sleep(4)


# write to blob
def write_random_numbers_to_blob():
    # Retrieve connection string from env set in manifest file.
    connection_string = os.getenv('STORAGE_ACCOUNT_CONNECTION_STRING')

    # creates an instance of the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "mycontainer"

    # creates an instance of the ContainerClient
    container_client = blob_service_client.get_container_client(container_name)
    # Create the root container if it doesn't already exist
    if not container_client.exists():
        container_client.create_container()

    blob_name = "numbers.txt"
    # Returns a new instance of the BlobClient class for the specified blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    while True:

        output_dict = {"temp": 0, "temp2": 1}

        # Check if the blob exists, if so download the data
        if blob_client.exists():
            # Get the current contents of the blob
            current_content = blob_client.download_blob().content_as_text()
        else:
            current_content = ""

        # Append the new random number to the current contents
        data = f"{current_content}\n{output_dict}"
        blob_client.upload_blob(data, blob_type="AppendBlob", overwrite=True)
        logging.info(f"Wrote {data} to blob storage")
        time.sleep(4)


# This method provides a way to read values from the redis instance from a local system
def read_from_redis_instance():
    # Use port forwarding to be able to connect to the redis instance
    redis_host = '127.0.0.1'
    redis_port = 6379

    # Create a Redis client object
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    numb = 0
    while True:
        # Retrieve hash values
        hash_key = 'key-' + str(numb)
        hash_values = r.hgetall(hash_key)

        # Convert byte strings to proper data types
        hash_values = {key.decode(): value.decode() for key, value in hash_values.items()}

        print(hash_values)

        time.sleep(4)


if __name__ == "__main__":
    write_random_numbers_to_redis()
