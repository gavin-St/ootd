from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv

import os

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "drip-index"

def query_by_vector(json_val, vector):
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
        
    index = pc.Index(index_name)
    namespace = json_val["type"] + "_PROD_01"
    query_results = index.query(
        namespace=namespace,
        vector=vector,
        top_k=3,
        include_values=False,
        include_metadata=True
    )
    return query_results["matches"]