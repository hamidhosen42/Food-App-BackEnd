from fastapi import APIRouter, HTTPException, status
from app.db.database import supabase
from app.schemas.user import UserCreate, UserLogin
from app.core.security import create_jwt_token
import time

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    try:
        print(f"DEBUG: Attempting to sign up user - Email: {user.email}")

        # Sign up user in Supabase Auth
        response = supabase.auth.sign_up({"email": user.email, "password": user.password})

        # Debugging: Print Supabase response
        print("DEBUG: Supabase signup response:", response)

        # Handle possible errors
        if "error" in response and response["error"]:
            error_message = response["error"]["message"].lower()
            print("ERROR:", error_message)

            if "email rate limit exceeded" in error_message:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many signup attempts. Try again later.")

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"]["message"])

        if "user" not in response or not response["user"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user in Supabase Auth")

        # Get the user ID from the response
        user_id = response["user"]["id"]

        # Insert user into 'users' table
        user_data = {
            "id": user_id,  # Use Supabase Auth user ID
            "name": user.name,
            "email": user.email,
            "created_at": "now()"  # Auto timestamp
        }

        insert_response = supabase.table("users").insert(user_data).execute()

        # Debugging: Print insert response
        print("DEBUG: Insert Response:", insert_response)

        if "error" in insert_response and insert_response["error"]:
            print("ERROR: Database insert failed:", insert_response["error"]["message"])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=insert_response["error"]["message"])

        return {
            "message": "User registered successfully",
            "user": {"id": user_id, "name": user.name, "email": user.email}
        }

    except HTTPException as http_exc:
        raise http_exc  # Allow HTTPExceptions to be returned directly

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/login")
def login(user: UserLogin):
    try:
        print(f"DEBUG: Attempting login for user - Email: {user.email}")

        response = supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})

        # Debugging: Print Supabase response
        print("DEBUG: Supabase login response:", response)

        if "error" in response and response["error"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"]["message"])

        if "user" not in response or not response["user"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid login response from Supabase")

        # Generate JWT Token
        token = create_jwt_token({"email": response["user"]["email"], "id": response["user"]["id"]})

        return {
            "message": "Login successful",
            "user": {
                "id": response["user"]["id"],
                "email": response["user"]["email"]
            },
            "access_token": token
        }

    except HTTPException as http_exc:
        raise http_exc  # Allow HTTPExceptions to be returned directly

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")