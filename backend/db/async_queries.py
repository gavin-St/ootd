from upsert import upsert_vector, upsert_bulk_vectors, query_index
from search import query_by_vector
from get_embedding import get_embedding

json = {
  "type": "Shoes",
  "color": "white",
  "brand": "Nike",
  "style": "sneakers",
  "material": "leather",
  "features": ["lace-up", "low-top", "rubber sole"],
  "additionalClothingProperties": ["Air cushioning"]
}

vector = get_embedding(json)
print(vector)
result = query_by_vector(json, vector)
print(result)