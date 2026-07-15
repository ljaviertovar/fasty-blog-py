from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str

    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAX_UPLOAD_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    POSTS_PER_PAGE: int = 10

    RESET_TOKEN_EXPIRE_MINUTES: int = 60

    MAIL_SERVER: str = "smtp.example.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: SecretStr = SecretStr("")
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_USE_TLS: bool = True

    FRONTEND_URL: str = "http://localhost:8000"

    S3_BUCKET_NAME: str = Field(validation_alias="S3_BUCKET_NAME")
    S3_ACCESS_KEY_ID: SecretStr | None = Field(
        default=None, validation_alias="S3_ACCESS_KEY_ID"
    )
    S3_SECRET_ACCESS_KEY: SecretStr | None = Field(
        default=None, validation_alias="S3_SECRET_ACCESS_KEY"
    )
    S3_REGION_NAME: str = Field(default="us-east-1", validation_alias="S3_REGION_NAME")
    S3_ENDPOINT_URL: str | None = (
        None  # Optional custom endpoint URL for S3-compatible services
    )


settings = Settings()  # type: ignore
