from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.authentication import routers as auth_routers
from app.api.wardrobe import routers as wardrobe_routers
from app.api.item import routers as item_routers
from app.api.category import routers as category_routers
from app.api.photo import routers as photos_routers
from app.api.admin import routers as admin_routers

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_groups = [
    auth_routers,
    wardrobe_routers,
    item_routers,
    category_routers,
    photos_routers,
    admin_routers,
]

for routers in router_groups:
    for router, prefix, tags in routers:
        app.include_router(router, prefix=prefix, tags=tags)
