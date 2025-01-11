import os

class Settings:
    app_name: str = "Quiz App"
    debug: bool = True

    @property
    def async_db_url(self) -> str:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", 5432)
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        db_url = (
            f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        return "postgresql+asyncpg://quiz_user:quiz_password@quiz_db:5432/quiz_db"



settings = Settings()

print("Async DB URL:", settings.async_db_url)
print("Debug Mode:", settings.debug)
