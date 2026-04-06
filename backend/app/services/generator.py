from abc import ABC, abstractmethod

from app.core.config import settings
from app.domain.models import GenerationMetadata, GenerationRequest, GenerationResponse
from app.domain.prompt_builder import PromptBuilder


class LLMClient(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class StubLLMClient(LLMClient):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        _ = system_prompt
        module_name = "top_module"
        for line in user_prompt.splitlines():
            if line.startswith("Target module name:"):
                module_name = line.split(":", 1)[1].strip() or module_name
                break
        return (
            f"module {module_name}(\n"
            "    input wire a,\n"
            "    input wire b,\n"
            "    output wire y\n"
            ");\n"
            "assign y = a & b;\n"
            "endmodule\n"
        )


class VerilogGeneratorService:
    def __init__(self, llm_client: LLMClient | None = None, prompt_builder: PromptBuilder | None = None) -> None:
        self.llm_client = llm_client or StubLLMClient()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        system_prompt = self.prompt_builder.load_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(request)
        verilog = self.llm_client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        return GenerationResponse(
            verilog_code=verilog,
            metadata=GenerationMetadata(
                prompt_version=settings.prompt_version,
                generator_name=self.llm_client.__class__.__name__,
            ),
            diagnostics=[],
        )
