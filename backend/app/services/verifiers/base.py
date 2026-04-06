from abc import ABC, abstractmethod

from app.domain.models import Diagnostic


class VerificationResult:
    def __init__(self, diagnostics: list[Diagnostic]) -> None:
        self.diagnostics = diagnostics


class Verifier(ABC):
    name: str

    @abstractmethod
    def verify(self, code: str) -> VerificationResult:
        raise NotImplementedError
