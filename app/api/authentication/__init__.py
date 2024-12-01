from app.api.authentication.register import router as register_router
from app.api.authentication.login import router as login_router
from app.api.authentication.logout import router as logout_router
from app.api.authentication.status import router as status_router

routers = [
    (register_router, "/api/authentication", ["authentication"]),
    (login_router, "/api/authentication", ["authentication"]),
    (logout_router, "/api/authentication", ["authentication"]),
    (status_router, "/api/authentication", ["authentication"]),
]
