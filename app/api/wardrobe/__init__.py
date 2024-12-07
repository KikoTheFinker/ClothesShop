from app.api.wardrobe.wardrobe import router as wardrobe_router

routers = [
    (wardrobe_router, "/api/wardrobes", ["wardrobe"]),
]
