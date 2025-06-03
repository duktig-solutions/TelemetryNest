# app/services/profile_service.py

from ..models import user as user_model

def get_profile_info(email: str):
    model = user_model.User()
    row = model.fetch_user_by_where({"email": email})
    if not row:
        return None
    return {
        'email': row['email'],
        'name': row['name']
    }
