# Natural Language to Verilog Generator

Monorepo for generating synthesizable Verilog-2001 from plain-English hardware descriptions.

## Structure
- `backend/`: FastAPI generation and verification pipeline
- `frontend/`: React UI
- `prompts/`: versioned system prompts
- `schemas/`: shared JSON schema contracts
- `examples/`: golden examples
- `tests/`: test suites
- `tools/`: utility wrappers (including future `iverilog` integration)

## Quickstart
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
