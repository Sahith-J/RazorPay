from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    woocommerce_url: str
    woocommerce_consumer_key: str
    woocommerce_consumer_secret: str

    request_timeout: int = 10
    max_retries: int = 3
    ollama_model: str = "qwen2.5:1.5b"
    ollama_host: str = "http://localhost:11434"

    frontend_url: str = "http://localhost:5173"
    verify_ssl: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()