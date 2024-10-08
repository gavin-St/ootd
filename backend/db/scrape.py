from serpapi import GoogleSearch
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from async_generate_data import generate_data

import json
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class Features(BaseModel):
    key: str
    value: str


class ClothingItem(BaseModel):
    imgUrl: str
    shoppingUrl: str
    gender: str
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
  "q": "essentials sweater",
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
                    "content": [
                        {
                            "type": "text",
                            "text": f"""
              JSON:
              {{ type: "Shoes" | "Jacket" | "Shirt" | "Pants" | "Dress" | "Hat" | "Glasses" | "Chain" | "Sweater" | "Skirt", gender: "Mens" | "Womens",
              color: "string", brightness: "string", brand: "string", "style": "string", material: "string", pattern: "string", features: {{}}, 
              additionalClothingProperties: [] }} 

              EXTRA_DATA:
              {{'title': "{product['title']}", 'source': "{product['source']}" }}

              Prompt:
              Based on the attached clothing image and EXTRA_DATA from the google product page, fill in the attached JSON file 
              along with any additional properties that can be observed on the clothing. Be very specific about color and pattern. Ignore sizing and condition details.
              """,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": product['thumbnail'],
                            },
                        },
                    ],
                },
            ],
            response_format=ClothingItem,
        )
        response_product = response.choices[0].message.parsed
        response_product.imgUrl = product["thumbnail"]
        response_product.shoppingUrl = product.get("link", "no-link")
        response_product.price = product["price"]
        clothing_items.append(response_product)

        # this is the json of the product
        json_result = response_product.dict()
        print(json_result)
        json_arr.append(json_result)

    return json_arr


generate_data(create_data_json_dump())
