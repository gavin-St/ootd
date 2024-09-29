from serpapi import GoogleSearch
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from get_embedding import create_embedding_from_json
from dotenv import load_dotenv
from upsert import upsert_vector, upsert_bulk_vectors, query_index

import json
import os
import time

def generate_data(json_arr):
  """
  Upserts every json in the array as a vector into the Pinecone database
  """

  # we want to insert as many vectors together as possible
  vectors_arr = []
  for json in json_arr:
    # this is the vector embedding of the product
    vector = create_embedding_from_json(json)
    vectors_arr.append(vector)

  upsert_bulk_vectors(json_arr, vectors_arr)
  time.sleep(10)
  query_index()

test_jsons = [
json.dumps({
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
}),
json.dumps({
  "type": "Jacket",
  "color": "Black",
  "brand": "Stone Island",
  "features": {
    "hood": True,
    "zipper": True,
    "material": "Waffle knit fabric",
    "patch_logo": "left sleeve"
  },
  "style": "casual",
  "additional_properties": {
    "pockets": "side",
    "cuffs": "ribbed",
    "fit": "relaxed"
  }
}),
json.dumps({
  "type": "T-shirt",
  "color": "White",
  "brand": "A Bathing Ape",
  "features": {
    "material": "Cotton",
    "graphic_design": "Purple Camo Ape Head",
    "logo_text": "A Bathing Ape",
    "neck_type": "Crewneck"
  },
  "style": "streetwear",
  "additional_properties": {
    "fit": "regular",
    "sleeve_type": "short sleeve",
    "graphic_position": "front",
    "print_style": "camo"
  }
})
]

print(type(test_jsons[0]))
print(type(test_jsons[1]))
generate_data(test_jsons)
