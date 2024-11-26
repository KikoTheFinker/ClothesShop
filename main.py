from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.authentication import routers as auth_routers

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
