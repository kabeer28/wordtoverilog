from fastapi import APIRouter

from app.core.config import settings
from app.domain.models import Diagnostic, GenerationRequest, GenerationResponse
from app.services.generator import VerilogGeneratorService
from app.services.postprocess import sanitize_output
from app.services.verifiers.iverilog import IverilogVerifier
from app.services.verifiers.static_rules import StaticRulesVerifier

router = APIRouter()


def _build_verifiers() -> list:
    verifiers = [StaticRulesVerifier()]
    if settings.enable_iverilog:
        verifiers.append(IverilogVerifier())
    return verifiers


@router.post("/generate", response_model=GenerationResponse)
def generate(request: GenerationRequest) -> GenerationResponse:
    service = VerilogGeneratorService()
    result = service.generate(request)
    result.verilog_code = sanitize_output(result.verilog_code)

    diagnostics: list[Diagnostic] = []
    for verifier in _build_verifiers():
        diagnostics.extend(verifier.verify(result.verilog_code).diagnostics)

    result.diagnostics = diagnostics
    return result
