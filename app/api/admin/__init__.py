from app.api.admin.admin import router as admin_router

routers = [
    (admin_router, "/api/admin", ["admin"]),
]