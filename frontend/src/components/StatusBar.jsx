function summarizeLatchStatus(diagnostics, hasOutput) {
  const latchIssues = diagnostics.filter((diag) => /latch/i.test(diag.message || ""));
  if (latchIssues.length > 0) {
    return { tone: "fail", label: `Latch Validation: Fail (${latchIssues.length})` };
  }
  if (hasOutput) {
    return { tone: "ok", label: "Latch Validation: Pass" };
  }
  return { tone: "warn", label: "Latch Validation: Pending" };
}

function summarizeIverilogStatus(diagnostics) {
  const iverilogDiags = diagnostics.filter((diag) => diag.source === "iverilog");
  if (iverilogDiags.length === 0) {
    return { tone: "warn", label: "Icarus Lint: Not Enabled" };
  }
  const hasError = iverilogDiags.some((diag) => diag.severity === "error");
  if (hasError) {
    return { tone: "fail", label: "Icarus Lint: Fail" };
  }
  return { tone: "ok", label: "Icarus Lint: Pass" };
}

export function StatusBar({ diagnostics, hasOutput }) {
  const latch = summarizeLatchStatus(diagnostics, hasOutput);
  const iverilog = summarizeIverilogStatus(diagnostics);

  return (
    <section className="status-bar">
      <div className={`status-chip ${latch.tone}`}>{latch.label}</div>
      <div className={`status-chip ${iverilog.tone}`}>{iverilog.label}</div>
    </section>
  );
}
