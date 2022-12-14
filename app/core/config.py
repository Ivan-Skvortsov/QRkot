from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):

    app_title: str = 'Фонд QRKot'
    app_description: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'Super secret key'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    # google api
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    # spreadsheet and drive settings
    spreadsheet_report_title: str = 'Отчет по закрытым проектам'
    spreadsheet_sheet_id: int = 0
    spreadsheet_api_version: str = 'v4'
    spreadsheet_api_name: str = 'sheets'
    google_drive_api_version: str = 'v3'
    google_drive_api_name: str = 'drive'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
