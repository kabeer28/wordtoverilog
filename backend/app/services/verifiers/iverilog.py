from app.domain.models import Diagnostic
from app.services.verifiers.base import VerificationResult, Verifier


class IverilogVerifier(Verifier):
    name = "iverilog"

    def verify(self, code: str) -> VerificationResult:
        _ = code
        return VerificationResult(
            diagnostics=[
                Diagnostic(
                    source=self.name,
                    severity="warning",
                    message="Icarus Verilog integration not enabled yet. Install/configure binary and activate verifier.",
                )
            ]
        )
