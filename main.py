from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.authentication import routers as auth_routers
from app.api.wardrobe import routers as wardrobe_routers
from app.api.item import routers as item_routers
from app.api.category import routers as category_routers
from app.api.photo import routers as photos_routers

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

for router, prefix, tags in auth_routers:
    app.include_router(router, prefix=prefix, tags=tags)

for router, prefix, tags in wardrobe_routers:
    app.include_router(router, prefix=prefix, tags=tags)

for router, prefix, tags in item_routers:
    app.include_router(router, prefix=prefix, tags=tags)

for route, prefix, tags in category_routers:
    app.include_router(route, prefix=prefix, tags=tags)

for router, prefix, tags in photos_routers:
    app.include_router(router, prefix=prefix, tags=tags)