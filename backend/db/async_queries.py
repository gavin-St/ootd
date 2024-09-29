from upsert import upsert_vector, upsert_bulk_vectors, query_index
from search import query_by_vector
from get_embedding import get_embedding
from get_attributes import get_attributes

json = get_attributes("/Users/gavinsong/Documents/ootd/backend/db/IMG_9618.jpg  ")

print(json)
vector = get_embedding(json)
print(vector)
result = query_by_vector(json, vector)
print(result)