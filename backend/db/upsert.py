from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv

import os

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "drip-index"

def upsert_vector(vector):
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

    index.upsert(
        vectors=[
            vector
        ],
        namespace="main-dripspace"
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

    vectors_to_upsert = [{'id': i, 'json': json[i], 'values': vector} for i, vector in enumerate(values_arr)]

    index.upsert(
        vectors=vectors_to_upsert,
        namespace="main-dripspace"
    )

def query_index():
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    index = pc.Index(index_name)
    print(index.describe_index_stats())
