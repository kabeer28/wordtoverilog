export function DiagnosticsPanel({ diagnostics }) {
  return (
    <section className="panel">
      <h2>Diagnostics</h2>
      {diagnostics.length === 0 ? (
        <p>No diagnostics.</p>
      ) : (
        <ul className="diagnostics-list">
          {diagnostics.map((diag, index) => (
            <li
              className={diag.severity === "error" ? "diag-error" : diag.severity === "warning" ? "diag-warning" : ""}
              key={`${diag.source}-${index}`}
            >
              [{diag.severity}] {diag.source}: {diag.message}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
