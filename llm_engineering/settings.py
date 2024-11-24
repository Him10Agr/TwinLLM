from  loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from zenml.client import Client
from zenml.exceptions import EntityExistsError

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    #OPENAI API
    OPENAI_MODEL_ID: str = "gpt-4o-mini"
    OPENAI_API_KEY: str | None = None

    #HUGGINGFACE 
    HUGGINGFACE_ACCESS_TOKEN: str | None = None

    #COMET LLM EXPERIMENTATION
    COMET_API_KEY: str | None = None
    COMET_PROJECT: str = "twinLLM"

    #MONGODB
    DATABASE_HOST: str | None = None
    #QDrantVDB
    #AWS Auth
    #AWS Sagemaker
    #RAG
    #LinkedIN Creds

    @property
    def OPENAI_MAX_TOKEN_WINDOW(self) -> int:

        max_token_window_official = {
            "gpt-3.5-turbo": 16385,
            "gpt-4-turbo": 128000,
            "gpt-4o": 128000,
            "gpt-4o-mini": 128000,
        }.get(self.OPENAI_MODEL_ID, 128000)

        return int(max_token_window_official * 0.9)

    @classmethod
    def load_settings(cls) -> "Settings":

        "Load settings from ZenML secret store or get default settings from .env"

        try:
            logger.info("Loading settings from ZenML secret store.")
            zenml_settings = Client().get_secret("TwinLLM_Settings")
            settings = Settings(**zenml_settings.secret_values)

        except(RuntimeError, KeyError):

            logger.warning(
                "Failed to load settings from zenml secret store. Loading from loacl .env file"
            )
            settings = Settings()
        
        return settings
    
    def export(self) -> None:

        "Push the settings to ZenML secret store"

        env_vars = self.model_dump()
        for key, value in env_vars.items():
            env_vars[key] = str(value)
        
        client = Client()
        try:
            client.create_secret(name="TwinLLM_Settings", values=env_vars)
        except EntityExistsError:
            logger.warning(
                "Secret scope already exists. Run 'zenml secret delete TwinLLM_Settings' to manually delete secret store before recreating it."
            )
    
if __name__ != "__main__":

    settings = Settings.load_settings()