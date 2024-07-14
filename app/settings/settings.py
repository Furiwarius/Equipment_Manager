import dotenv
import os

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
TEST_DATABASE = os.getenv("TEST_DATABASE")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("HOST")
DATABASE_LOG_SETTINGS = os.getenv("DATABASE_LOG_SETTINGS")
DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL")