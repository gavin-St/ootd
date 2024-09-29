from serpapi import GoogleSearch
import os
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import json
from get_embedding import create_embedding_from_json
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

class Features(BaseModel):
  key: str
  value: str

class ClothingItem(BaseModel):
  imgUrl: str
  shoppingUrl: str
  type: str
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
  "q": "mens hoodies",
  "hl": "en",
  "gl": "us",
  "location": "United States",
  "direct_link": "true"
}

search = GoogleSearch(params)
results = search.get_dict()

client = OpenAI()

def create_data_json_dump():
  """
  Creates a big json file of all clothing data scraped
  """
  clothing_items = []
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
    clothing_items.append(response_product)

  clothing_items_json = [item.dict() for item in clothing_items]
  return json.dumps(clothing_items_json, indent=2)


jsonDumped = create_data_json_dump()
vector = create_embedding_from_json(jsonDumped)
print(vector)
