from app.api.photo.photo import router as photo_router

routers = [
    (photo_router, "/api", ["photo"]),
]
