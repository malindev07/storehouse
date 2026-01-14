import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_BRAND: str | None = os.environ.get("DB_BRAND")
    DB_ENGINE: str | None = os.environ.get("DB_ENGINE")
    DB_USER: str | None = os.environ.get("DB_USER")
    DB_PASSWORD: str | None = os.environ.get("DB_PASSWORD")
    DB_HOST: str | None = os.environ.get("DB_HOST")
    DB_PORT: str | None = os.environ.get("DB_PORT")
    DB_NAME: str | None = os.environ.get("DB_NAME")

    @property
    def database_url(self) -> str:

        return (
            f"{self.DB_BRAND}+{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}"
            f":{self.DB_PORT}/{self.DB_NAME}"
        )
