# Food-App-BackEnd


1️⃣ Folder Structure:

```
📂 fastapi_food_app
│── 📂 app
│   │── 📂 api
│   │   │── 📂 routes
│   │   │   │── auth.py
│   │   │   │── users.py
│   │   │   │── food.py
│   │   │── __init__.py
│   │── 📂 core
│   │   │── config.py
│   │   │── security.py
│   │── 📂 db
│   │   │── database.py
│   │   │── models.py
│   │   │── crud.py
│   │── 📂 schemas
│   │   │── user.py
│   │   │── food.py
│   │── main.py
│── .env
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── README.md
```

---

2️⃣ Install Dependencies


pip install fastapi uvicorn supabase pyjwt passlib sqlalchemy psycopg2 pydantic

---

3️⃣ Configure Supabase (core/config.py)

```
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your-supabase-api-key
SECRET_KEY=your-secret-key


```

---

4️⃣ Database Setup (db/database.py)

from supabase import create_client
from core.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

---

5️⃣ Models (db/models.py)

```
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
```

---

6️⃣ Authentication (api/routes/auth.py)

```
from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.user import UserCreate, UserLogin
from core.security import create_jwt_token

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    response = supabase.auth.sign_up(user.email, user.password)
    if "error" in response:
        raise HTTPException(status_code=400, detail="Signup failed")
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    response = supabase.auth.sign_in(email=user.email, password=user.password)
    if "error" in response:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt_token(user.email)
    return {"token": token}
```

---

7️⃣ JWT Token Handling (core/security.py)

```
import jwt
import datetime
from core.config import SECRET_KEY

def create_jwt_token(email: str):
    token = jwt.encode({"sub": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, SECRET_KEY, algorithm="HS256")
    return token
```

---

8️⃣ CRUD for Users (db/crud.py)

```
def get_user_by_email(email: str):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def create_user(email: str, password: str):
    return supabase.table("users").insert({"email": email, "password": password}).execute()

```

---

9️⃣ Food Items (api/routes/food.py)

```
from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.food import FoodItem

router = APIRouter()

@router.get("/items")
def get_food_items():
    response = supabase.table("food_items").select("*").execute()
    return response.data

@router.post("/items")
def add_food_item(item: FoodItem):
    response = supabase.table("food_items").insert(item.dict()).execute()
    return response.data
```

---

🔟 API Entry (main.py)

```
from fastapi import FastAPI
from api.routes import auth, food

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/food", tags=["Food"])
```

---

🔹 Running the Server
uvicorn app.main:app --reload
