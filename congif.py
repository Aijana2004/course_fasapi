from dotenv import load_dotenv
import os


load_dotenv()


SEKRET_KEY = os.getenv('SEKRET_KEY')


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 2


class Settings:
    CLIENT_ID_GITHUB = os.getenv('CLIENT_ID_GITHUB')
    GITHUB_KEY = os.getenv('GITHUB_KEY')
    GITHUB_LOGIN_CALLBACK = os.getenv('GITHUB_LOGIN_CALLBACK')


class Setting:
    GOOGLE_KEY = os.getenv('GOOGLE_KEY')
    GOOGLE_ID_CLIENT = os.getenv('GOOGLE_ID_CLIENT')
    GOOGLE_LOGIN_CALLBACK = os.getenv('GOOGLE_LOGIN_CALLBACK')


settings = Settings()
setting = Setting()

