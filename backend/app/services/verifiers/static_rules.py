from app.domain.models import Diagnostic
from app.services.postprocess import run_deterministic_checks
from app.services.verifiers.latch_checker import find_latch_inference_issues
from app.services.verifiers.base import VerificationResult, Verifier


class StaticRulesVerifier(Verifier):
    name = "static_rules"

    def verify(self, code: str) -> VerificationResult:
        messages = run_deterministic_checks(code)
        messages.extend(find_latch_inference_issues(code))

        diagnostics = [
            Diagnostic(source=self.name, severity="error", message=message)
            for message in messages
        ]
        return VerificationResult(diagnostics=diagnostics)
