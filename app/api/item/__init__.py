from app.api.item.item import router as wardrobe_router

routers = [
    (wardrobe_router, "/api", ["item"]),
]
