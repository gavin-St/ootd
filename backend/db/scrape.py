from serpapi import GoogleSearch
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from get_embedding import create_embedding_from_json
from dotenv import load_dotenv
from upsert import upsert_vector, upsert_bulk_vectors, query_index
from generate_data import generate_data

import json
import os

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

class Features(BaseModel):
  key: str
  value: str

class ClothingItem(BaseModel):
  imgUrl: str
  shoppingUrl: str
  type: str
  price: str
  color: str
  brand: str
  style: str
  material: str
  features: List[Features]
  additionalClothingProperties: List[str]

params = {
  "api_key": os.getenv("SCRAPER_API_KEY"),
  "engine": "google_shopping",
  "google_domain": "google.com",
  "q": "mens shoes",
  "hl": "en",
  "gl": "us",
  "location": "United States",
  "direct_link": "true"
}

vectors_arr = []
json_arr = []
clothing_items = []

def create_data_json_dump():
    """
    Creates a big json file of all clothing data scraped
    """
    search = GoogleSearch(params)
    results = search.get_dict()

    client = OpenAI()
    for product in results.get("shopping_results", []):
      response = client.beta.chat.completions.parse(
      model="gpt-4o-mini",
      messages=[
          {
              "role": "user",
              "content": f'''
              JSON:
              {{ type: "Shoes" | "Jacket" | "Shirt" | "Pants" | "Dress" | "Hat" | "Glasses" | "Chain" | "Sweater" | "Skirt", 
              color: "string", brand: "string", "style": "string", material: "string", features: {{}}, 
              additionalClothingProperties: [] }} 

              EXTRA_DATA:
              {{'title': "{product['title']}", 'source': "{product['source']}" }}

              Prompt:
              Based on the attached clothing image and EXTRA_DATA from the google product page, fill in the attached JSON file 
              along with any additional properties that can be observed on the clothing. Ignore sizing details.
              '''
          },
      ],
      response_format=ClothingItem,
      )
      response_product = response.choices[0].message.parsed
      response_product.imgUrl = product["thumbnail"]
      response_product.shoppingUrl = product["link"]
      response_product.price = product["price"]
      clothing_items.append(response_product)

      # this is the json of the product
      json_dump = json.dumps(response_product.dict(), indent=2)
      print(json_dump)
      json_arr.append(json_dump)
        
    return json_arr

generate_data(create_data_json_dump())