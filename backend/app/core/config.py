import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODEL_PATH: str = "models/house_price_production_rf.pkl"
    LOCATION_PRICE_MAP_PATH: str = "models/location_price_map.json"
    MODEL_DEFAULTS_PATH: str = "models/model_defaults.json"
    MODEL_OPTIONS_PATH: str = "models/model_options.json"
    MODEL_VERSION: str = "1.0"
    APP_NAME: str = "House Price Prediction API"
    LOG_LEVEL: str = "INFO"

    # Settings config: specify env file location
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
