from fastapi import APIRouter, HTTPException
from app.db.database import supabase
from app.schemas.food import FoodItem 


router = APIRouter()

@router.get("/items")
def get_food_items():
    response = supabase.table("food_items").select("*").execute()
    return response.data

@router.post("/items")
def add_food_item(item: FoodItem):
    response = supabase.table("food_items").insert(item.dict()).execute()
    return response.data
