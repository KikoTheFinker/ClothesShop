from app.api.category.category import router as category_router

routers = [
    (category_router, "/api", ["category"]),
]
