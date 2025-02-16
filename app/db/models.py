from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    email: str
    password: str

class FoodItem(BaseModel):
    id: int
    name: str
    price: float
    rating: float
    image_url: str
