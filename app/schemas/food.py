from pydantic import BaseModel

class FoodItem(BaseModel):
    name: str
    price: float
    rating: float
    image_url: str