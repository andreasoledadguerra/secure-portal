from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Aplicación ---
    PROJECT_NAME: str = "Secure Volunteer Portal"
    API_V1_PREFIX: str = "/api/v1"

    # --- Base de datos ---
    # URL con driver asyncpg (para SQLAlchemy async)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/svp_db"

    # --- Seguridad / JWT ---
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TEMP_TOKEN_EXPIRE_MINUTES: int = 15

    # --- MFA / bloqueo ---
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_MINUTES: int = 15

    # --- TOTP ---
    TOTP_INTERVAL_SECONDS: int = 30
    TOTP_DIGITS: int = 6
    TOTP_WINDOW: int = 5  # ±1 intervalo de tolerancia

    # --- Carga desde .env ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()