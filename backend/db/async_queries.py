from upsert import upsert_vector, upsert_bulk_vectors, query_index
from search import query_by_vector
from get_embedding import create_embedding_from_json

import json

original_json = json.dumps({
  "type": "Shoes",
  "color": "White",
  "brand": "New Balance",
  "style": "Sneaker",
  "material": "Mesh and Synthetic",
  "features": ["Laces", "Logo on the side", "Reinforced heel"],
  "additionalClothingProperties": ["Athletic design", "Cushioned sole"]
})

vector = create_embedding_from_json(original_json)
print(vector)
result = query_by_vector(vector)
print(result)