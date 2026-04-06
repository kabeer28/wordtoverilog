const API_BASE = "http://localhost:8000/api/v1";

export async function generateVerilog(payload) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Generation request failed: ${response.status}`);
  }

  return response.json();
}
