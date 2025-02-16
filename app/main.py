from fastapi import FastAPI
from app.api.routes import auth, food  

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/food", tags=["Food"])