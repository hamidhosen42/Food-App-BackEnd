import supabase


def get_user_by_email(email: str):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def create_user(email: str, password: str):
    return supabase.table("users").insert({"email": email, "password": password}).execute()
