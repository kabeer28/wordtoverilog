export function ConstraintOptions({ moduleName, onModuleNameChange }) {
  return (
    <section className="panel">
      <h2>Constraints</h2>
      <label htmlFor="moduleName">Module name</label>
      <input
        className="input-field"
        id="moduleName"
        type="text"
        value={moduleName}
        onChange={(event) => onModuleNameChange(event.target.value)}
        placeholder="top_module"
      />
    </section>
  );
}
