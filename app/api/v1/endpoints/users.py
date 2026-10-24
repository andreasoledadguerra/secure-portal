from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "mfa_enabled": current_user.mfa_enabled}