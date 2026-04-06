import re


FORBIDDEN_PATTERNS = [
    r"\binitial\b",
    r"#\s*(\d+|\([^)]+\)|[A-Za-z_][A-Za-z0-9_]*)",
]


def sanitize_output(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    return cleaned + "\n"


def run_deterministic_checks(code: str) -> list[str]:
    errors: list[str] = []

    if not re.search(r"\bmodule\b[\s\S]*\bendmodule\b", code):
        errors.append("Missing module/endmodule wrapper.")

    if not re.search(r"\bmodule\s+\w+\s*\(", code):
        errors.append("Module header must include explicit port list.")

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code):
            errors.append(f"Forbidden construct detected: {pattern}")

    if "always_comb" in code or "logic " in code:
        errors.append("Use Verilog-2001 constructs only; SystemVerilog keywords detected.")

    # Conservative latch checks: explicit latch intent or incomplete combinational branches.
    if re.search(r"\blatch\b", code, flags=re.IGNORECASE):
        errors.append("Latch behavior is forbidden for synthesizable RTL in this engine.")

    if "always @(*)" in code and re.search(r"\bif\s*\([^)]+\)\s*[^;{]+;\s*(?!\s*else)", code):
        errors.append(
            "Potential latch inference detected: combinational if/else appears incomplete. "
            "Provide defaults and full assignment coverage."
        )

    return errors
