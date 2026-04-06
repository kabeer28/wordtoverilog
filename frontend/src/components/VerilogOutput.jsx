const VERILOG_KEYWORDS = new Set([
  "module",
  "endmodule",
  "input",
  "output",
  "inout",
  "wire",
  "reg",
  "assign",
  "always",
  "begin",
  "end",
  "if",
  "else",
  "case",
  "endcase",
  "default",
  "posedge",
  "negedge",
  "parameter"
]);

function renderLine(line, lineKey) {
  if (line.trim().startsWith("//")) {
    return (
      <div key={lineKey}>
        <span className="tok-comment">{line}</span>
      </div>
    );
  }

  const parts = line.split(/(\b[A-Za-z_][A-Za-z0-9_]*\b|\b\d+\b|[(){}\[\];,:])/g);
  return (
    <div key={lineKey}>
      {parts.map((part, idx) => {
        if (!part) return null;
        if (VERILOG_KEYWORDS.has(part)) {
          return (
            <span className="tok-keyword" key={`${lineKey}-${idx}`}>
              {part}
            </span>
          );
        }
        if (/^\d+$/.test(part)) {
          return (
            <span className="tok-number" key={`${lineKey}-${idx}`}>
              {part}
            </span>
          );
        }
        if (/^[(){}\[\];,:]$/.test(part)) {
          return (
            <span className="tok-symbol" key={`${lineKey}-${idx}`}>
              {part}
            </span>
          );
        }
        return <span key={`${lineKey}-${idx}`}>{part}</span>;
      })}
    </div>
  );
}

export function VerilogOutput({ code }) {
  const text = code || "No output yet.";
  const lines = text.split("\n");
  return (
    <section className="panel">
      <h2>Generated Verilog</h2>
      <pre className="code-block">
        <code>{lines.map((line, idx) => renderLine(line, idx))}</code>
      </pre>
    </section>
  );
}
