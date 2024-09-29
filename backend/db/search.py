from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv

import os

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

def query_by_vector(vector):
    query_results = index.query(
        namespace="main-dripspace",
        vector=vector,
        top_k=4,
        include_values=False
    )
    return query_results[matches]