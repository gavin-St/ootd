from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv

import os

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

def query_by_vector(vector):
    query_results1 = index.query(
        namespace="example-namespace1",
        vector=[1.0, 1.5],
        top_k=3,
        include_values=True
    )