from pathlib import Path

from app.domain.models import GenerationRequest
from app.domain.prompt_builder import PromptBuilder


def test_prompt_builder_loads_v1() -> None:
    root = Path(__file__).resolve().parents[2] / "prompts" / "verilog_system"
    builder = PromptBuilder(prompt_root=root)
    text = builder.load_system_prompt("v1")
    assert "synthesizable" in text.lower()


def test_prompt_builder_renders_user_prompt() -> None:
    builder = PromptBuilder(prompt_root=Path("/tmp"))
    request = GenerationRequest(description="Create a counter", module_name="counter8")
    user_prompt = builder.build_user_prompt(request)
    assert "counter8" in user_prompt
    assert "Create a counter" in user_prompt
