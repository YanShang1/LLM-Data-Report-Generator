import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )
