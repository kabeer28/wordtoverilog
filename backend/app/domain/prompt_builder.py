from pathlib import Path

from app.core.config import settings
from app.domain.models import GenerationRequest


class PromptBuilder:
    def __init__(self, prompt_root: Path | None = None) -> None:
        self.prompt_root = prompt_root or Path(__file__).resolve().parents[3] / "prompts" / "verilog_system"

    def load_system_prompt(self, version: str | None = None) -> str:
        selected = version or settings.prompt_version
        path = self.prompt_root / f"{selected}.md"
        return path.read_text(encoding="utf-8")

    def build_user_prompt(self, request: GenerationRequest) -> str:
        module_name = request.module_name or "top_module"
        constraints = request.constraints.model_dump(exclude_none=True) if request.constraints else {}
        lines = [
            "Generate synthesizable Verilog-2001 for this circuit description:",
            request.description.strip(),
            f"Target module name: {module_name}",
        ]
        if constraints:
            lines.append(f"Constraints: {constraints}")
        return "\n".join(lines)
