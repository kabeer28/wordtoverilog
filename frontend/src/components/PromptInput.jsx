export function PromptInput({ value, onChange }) {
  return (
    <section className="panel">
      <h2>Circuit Description</h2>
      <textarea
        className="textarea-field"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Describe the digital circuit in plain English..."
      />
    </section>
  );
}
