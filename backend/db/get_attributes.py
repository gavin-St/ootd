import base64
import requests
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
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
    type: str
    price: str
    color: str
    brand: str
    style: str
    material: str
    features: List[Features]
    additionalClothingProperties: List[str]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_attributes(image_path):
    """
    Takes the local image path and gets the attributes in json format needed to query database
    """
    base64_image = encode_image(image_path)

    client = OpenAI()
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
              {{ type: "Shoes" | "Jacket" | "Shirt" | "Pants" | "Dress" | "Hat" | "Glasses" | "Chain" | "Sweater" | "Skirt", 
              color: "string", brand: "string", "style": "string", material: "string", pattern: "string", features: {{}}, 
              additionalClothingProperties: [] }} 

              Prompt:
              Based on the attached clothing image fill in the attached JSON file along with any additional unique properties that can be observed on the clothing. Ignore sizing and condition details.
              """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
        response_format=ClothingItem,
    )
    response_product = response.choices[0].message.parsed
    return response_product.dict()
