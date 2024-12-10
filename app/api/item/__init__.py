from app.api.item.item import router as item_router

routers = [
    (item_router, "/api", ["item"]),
]
