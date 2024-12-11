import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
