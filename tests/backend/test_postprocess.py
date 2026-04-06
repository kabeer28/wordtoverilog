from app.services.postprocess import run_deterministic_checks


def test_rejects_initial_block() -> None:
    code = """
module demo(input wire a, output reg y);
initial begin
  y = a;
end
endmodule
"""
    errors = run_deterministic_checks(code)
    assert any("Forbidden construct" in error for error in errors)


def test_accepts_simple_module() -> None:
    code = """
module and2(
  input wire a,
  input wire b,
  output wire y
);
assign y = a & b;
endmodule
"""
    errors = run_deterministic_checks(code)
    assert errors == []
