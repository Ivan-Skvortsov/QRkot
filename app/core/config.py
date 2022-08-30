from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):

    app_title: str = 'Фонд QRKot'
    app_description: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'Super secret key'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
