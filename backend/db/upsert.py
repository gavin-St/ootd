from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
from collections.abc import MutableMapping

import os
import json
import uuid
import time

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "drip-index"

def upsert_vector(json_val, vector):
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
        
    index = pc.Index(index_name)
    namespace = json_val["gender"] + json_val["type"] + "_PROD_01"
    index.upsert(
        vectors=[
            {'id': str(uuid.uuid4()), 'metadata': flatten(json_val), values: vector}
        ],
        namespace=namespace
    )

def upsert_bulk_vectors(json_arr, values_arr):
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
        
    index = pc.Index(index_name)

    vectors_to_upsert = [{'id': str(uuid.uuid4()), 'metadata': flatten(json_arr[i]), 'values': vector} for i, vector in enumerate(values_arr)]
    
    namespace = "Womens" + json_arr[0]["type"] + "_PROD_01"

    index.upsert(
        vectors=vectors_to_upsert,
        namespace=namespace
    )

    namespace = "Mens" + json_arr[0]["type"] + "_PROD_01"

    index.upsert(
        vectors=vectors_to_upsert,
        namespace=namespace
    )

def query_index():
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    index = pc.Index(index_name)
    print(index.describe_index_stats())

def flatten(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        
        if isinstance(value, MutableMapping):
            # If the value is a dictionary, recurse into it
            items.extend(flatten(value, new_key, separator=separator).items())
        elif isinstance(value, list):
            # If the value is a list, check if it's a list of dictionaries
            for index, item in enumerate(value):
                if isinstance(item, MutableMapping):
                    # Flatten each dictionary in the list
                    items.extend(flatten(item, f"{new_key}{separator}{index}", separator=separator).items())
                else:
                    # Handle non-dictionary items in the list
                    items.append((f"{new_key}{separator}{index}", item))
        else:
            # For normal key-value pairs
            items.append((new_key, value))
    
    return dict(items)
