from pydantic import BaseModel, Field


class GenerationConstraints(BaseModel):
    clock_name: str | None = None
    reset_name: str | None = None
    reset_active: str | None = None


class GenerationRequest(BaseModel):
    description: str = Field(min_length=1)
    module_name: str | None = None
    constraints: GenerationConstraints | None = None


class Diagnostic(BaseModel):
    source: str
    severity: str
    message: str


class GenerationMetadata(BaseModel):
    prompt_version: str
    generator_name: str


class GenerationResponse(BaseModel):
    verilog_code: str
    metadata: GenerationMetadata
    diagnostics: list[Diagnostic] = Field(default_factory=list)
