from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'myapp'
    environment: str = 'dev'
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix='MYAPP_',
        extra='ignore',
    )
