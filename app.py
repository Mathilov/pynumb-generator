import os
import time
import random
import redis
import logging

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobClient, BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

# constructs a connection string for the Azure Blob Storage.
storage_account_name = os.getenv('storage_account_name')
storage_account_key = os.getenv('storage_account_key')
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"


# Retrieves the Redis server host and port from the environment variables or set default values if they are not provided.
redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

# Creates a Redis client instance named cache using the host, port, and database number.
cache = redis.Redis(host=redis_host, port=redis_port, db=0)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "mycontainer"
container_client = blob_service_client.get_container_client(container_name)

# Create the root container if it doesn't already exist
if not container_client.exists():
    container_client.create_container()
blob_name = "numbers.txt"
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# write to redis instance
def write_random_numbers_to_redis():
    while True:
        random_number = random.randint(1, 100)
        cache.rpush('random_numbers', random_number)
        logging.info(f"Wrote {random_number} to Redis")
        time.sleep(10)

#write to blob
def write_random_numbers_to_blob():
    # creates a client instance


    while True:
        random_number = random.randint(1, 100)
        if blob_client.exists():
            current_content = blob_client.download_blob().content_as_text()
        else:
            current_content = ""
        # Get the current contents of the blob

        # Append the new random number to the current contents
        data = f"{current_content}\n{random_number}"
        blob_client.upload_blob(data, blob_type="AppendBlob", overwrite=True)
        logging.info(f"Wrote {data} to blob storage")
        time.sleep(10)



if __name__ == "__main__":
    write_random_numbers_to_blob()