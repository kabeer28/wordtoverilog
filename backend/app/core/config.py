from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "NL2Verilog API"
    prompt_version: str = "v1"
    enabled_verifiers: list[str] = Field(default_factory=lambda: ["static_rules"])
    enable_iverilog: bool = False


settings = Settings()
