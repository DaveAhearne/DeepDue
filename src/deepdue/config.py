from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ch_api_key: str

    langsmith_tracing: str = "true"
    langsmith_endpoint: str = ""
    langsmith_api_key: str = ""
    langsmith_project: str = "deepdue"
    
    host: str = "0.0.0.0"
    port: int = 1234
    workers: int = 1

    log_level: str = "INFO"

    llm_provider: str = "ollama"
    llm_base_url: str = "http://localhost:11434"
    
    llm_extraction_model: str = "llama3.1:8b"
    llm_reasoning_model: str = "llama3.1:8b"
    llm_synthesis_model: str = "llama3.1:8b"

settings = Settings()