from app.api.user.user import router as user_router

routers = [
    (user_router, "/api/user", ["user"]),
]