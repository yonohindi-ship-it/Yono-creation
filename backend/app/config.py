from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    jwt_secret: str = "CHANGE_ME"
    jwt_expire_minutes: int = 10080
    database_url: str = "sqlite:///./yono_ai.db"
    cors_origins: str = "http://localhost:8081"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    leonardo_api_key: str = ""
    leonardo_model_id: str = ""
    kling_api_key: str = ""
    kling_base_url: str = "https://api-singapore.klingai.com"
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def origins(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings = Settings()
