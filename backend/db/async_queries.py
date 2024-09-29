from upsert import upsert_vector, upsert_bulk_vectors, query_index
from search import query_by_vector
from get_embedding import get_embedding

import json

original_json = {
  "type": "Shoes",
  "color": "White",
  "brand": "New Balance",
  "style": "Sneaker",
  "material": "Mesh and Synthetic",
  "features": ["Laces", "Logo on the side", "Reinforced heel"],
  "additionalClothingProperties": ["Athletic design", "Cushioned sole"]
}

vector = get_embedding(original_json)
print(vector)
result = query_by_vector(vector)
print(result)