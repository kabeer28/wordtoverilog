# NL2Verilog Architecture

This repository uses a monorepo layout with:
- `backend/`: FastAPI service and generation pipeline
- `frontend/`: React user interface
- `prompts/`: versioned system prompts
- `schemas/`: shared API contracts
- `tests/`: backend and frontend tests

Validation is modeled as a pluggable pipeline where static checks run first,
followed by optional external tool adapters (for example `iverilog`).
