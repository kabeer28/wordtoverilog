from app.services.verifiers.latch_checker import find_latch_inference_issues


def test_latch_checker_accepts_defaulted_comb_logic() -> None:
    code = """
module mux2(
  input wire sel,
  input wire a,
  input wire b,
  output reg y
);
always @(*) begin
  y = a;
  if (sel) begin
    y = b;
  end
end
endmodule
"""
    issues = find_latch_inference_issues(code)
    assert issues == []


def test_latch_checker_flags_if_without_else() -> None:
    code = """
module bad_if(
  input wire en,
  input wire d,
  output reg q
);
always @(*) begin
  if (en) begin
    q = d;
  end
end
endmodule
"""
    issues = find_latch_inference_issues(code)
    assert any("if branch without else" in issue for issue in issues)


def test_latch_checker_flags_case_without_default() -> None:
    code = """
module bad_case(
  input wire [1:0] sel,
  input wire a,
  input wire b,
  output reg y
);
always @(*) begin
  case (sel)
    2'b00: y = a;
    2'b01: y = b;
  endcase
end
endmodule
"""
    issues = find_latch_inference_issues(code)
    assert any("case without default" in issue for issue in issues)
