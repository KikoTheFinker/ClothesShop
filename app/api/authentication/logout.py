from fastapi import APIRouter, Response

router = APIRouter()


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
