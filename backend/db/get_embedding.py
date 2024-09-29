from openai import OpenAI
from dotenv import load_dotenv
from upsert import upsert_vector, upsert_bulk_vectors, query_index

import json
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embedding_from_json(data):
    """
    Converts the given JSON object into a text embedding vector using OpenAI's embedding model.
    """
    # Serialize the JSON data to a descriptive string
    serialized_string = json.dumps(data)

    # Generate the embedding using OpenAI's model
    response = client.embeddings.create(model="text-embedding-ada-002",  # Most cost-effective model for embedding tasks
    input=serialized_string)

    # Extract the embedding vector (the first embedding in the list)
    embedding_vector = response.data[0].embedding

    return embedding_vector

# Example JSON object
json_data = {
  "type": "Sweater",
  "color": "Black",
  "brand": "Amiri",
  "features": {
    "material": "Cotton",
    "logo_text": "Amiri Motions M.A. Auto District, CA",
    "neck_type": "Crewneck"
  },
  "style": "casual",
  "additional_properties": {
    "fit": "regular",
    "sleeve_type": "long sleeve",
    "embroidery": "yes",
    "patch_position": "left chest"
  }
}

# query_index()
