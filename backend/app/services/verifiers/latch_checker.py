import re


ASSIGN_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b(?:\s*\[[^\]]+\])?\s*=")


def _extract_always_comb_blocks(code: str) -> list[str]:
    blocks: list[str] = []
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "always @(*)" not in line:
            i += 1
            continue

        block_lines: list[str] = [line]
        begin_depth = line.count("begin") - line.count("end")
        i += 1

        while i < len(lines):
            block_lines.append(lines[i])
            begin_depth += lines[i].count("begin") - lines[i].count("end")
            if begin_depth <= 0 and "begin" in block_lines[0]:
                break
            if begin_depth <= 0 and "begin" not in block_lines[0]:
                break
            i += 1

        blocks.append("\n".join(block_lines))
        i += 1
    return blocks


def _assigned_signals(text: str) -> set[str]:
    return {match.group(1) for match in ASSIGN_RE.finditer(text)}


def _default_assignment_region(block: str) -> str:
    """
    Return the top region of a combinational block before the first control-flow
    statement. Assignments found here are treated as safe defaults.
    """
    lines = block.splitlines()
    region: list[str] = []
    for line in lines:
        if re.search(r"\b(if|case)\b", line):
            break
        region.append(line)
    return "\n".join(region)


def _if_without_else_present(text: str) -> bool:
    # Conservative heuristic: if there is an if statement and no else in the block.
    return bool(re.search(r"\bif\s*\(", text)) and "else" not in text


def _case_without_default_present(text: str) -> bool:
    if "case" not in text:
        return False
    for case_match in re.finditer(r"\bcase\b[\s\S]*?\bendcase\b", text):
        case_body = case_match.group(0)
        if "default" not in case_body:
            return True
    return False


def find_latch_inference_issues(code: str) -> list[str]:
    issues: list[str] = []
    blocks = _extract_always_comb_blocks(code)

    for idx, block in enumerate(blocks, start=1):
        all_assigned = _assigned_signals(block)
        if not all_assigned:
            continue

        default_assigned = _assigned_signals(_default_assignment_region(block))

        if _if_without_else_present(block):
            maybe_latch = sorted(all_assigned - default_assigned)
            if maybe_latch:
                issues.append(
                    f"Potential latch inference in always @(*) block {idx}: "
                    f"if branch without else may leave signals unassigned ({', '.join(maybe_latch)})."
                )

        if _case_without_default_present(block):
            maybe_latch = sorted(all_assigned - default_assigned)
            if maybe_latch:
                issues.append(
                    f"Potential latch inference in always @(*) block {idx}: "
                    f"case without default may leave signals unassigned ({', '.join(maybe_latch)})."
                )

    return issues
