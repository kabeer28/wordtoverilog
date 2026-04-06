import { useState } from "react";
import { generateVerilog } from "../api/client";
import { ConstraintOptions } from "../components/ConstraintOptions";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { PromptInput } from "../components/PromptInput";
import { StatusBar } from "../components/StatusBar";
import { VerilogOutput } from "../components/VerilogOutput";

export function GeneratePage() {
  const [description, setDescription] = useState("");
  const [moduleName, setModuleName] = useState("top_module");
  const [verilogCode, setVerilogCode] = useState("");
  const [diagnostics, setDiagnostics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await generateVerilog({ description, module_name: moduleName });
      setVerilogCode(result.verilog_code || "");
      setDiagnostics(result.diagnostics || []);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <div className="app-container">
        <div className="header-row">
          <div>
            <h1 className="header-title">Natural Language to Verilog</h1>
            <p className="header-subtitle">ASIC-grade RTL generation workspace</p>
          </div>
        </div>

        <StatusBar diagnostics={diagnostics} hasOutput={Boolean(verilogCode)} />

        <form onSubmit={onSubmit}>
          <div className="grid-two-pane">
            <div>
              <PromptInput value={description} onChange={setDescription} />
              <ConstraintOptions moduleName={moduleName} onModuleNameChange={setModuleName} />
            </div>
            <VerilogOutput code={verilogCode} />
          </div>

          <div className="controls-row">
            <button className="primary-btn" type="submit" disabled={loading || !description.trim()}>
              {loading ? "Generating..." : "Generate Verilog"}
            </button>
            {error ? <p className="error-text">{error}</p> : null}
          </div>
        </form>

        <DiagnosticsPanel diagnostics={diagnostics} />
      </div>
    </main>
  );
}
