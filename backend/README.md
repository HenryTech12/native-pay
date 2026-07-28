# NativePay Backend — Python (FastAPI)

Drop-in replacement for `backend/` (the TypeScript/Express version) — identical routes, identical request/response shapes, same state machine logic, verified against the same test cases. Point the existing `frontend/` at whichever one you run; nothing on the frontend needs to change.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in GROQ_API_KEY at minimum
uvicorn app.main:app --reload --port 4000
```
Runs on `http://localhost:4000` — same port as the TS backend, so `frontend/.env`'s `VITE_API_BASE` doesn't need to change when switching between them (just don't run both at once on the same port).

## Tests
```bash
pytest tests/ -v
```
Same 9 cases as the TypeScript suite: invalid amount, unknown recipient, low-confidence clarification, the confirm→face-verify→send→success happy path, blocked out-of-order execution, idempotency, and cancellation. All pass.

## Structure
```
app/
  main.py                    FastAPI routes
  models.py                  Pydantic models (mirrors types.ts)
  services/
    groq_service.py            Whisper STT + LLM intent parsing
    bmoni_service.py           BMONIService — mock/sandbox adapter
    transaction_service.py     State machine, server-side validation
    voice_auth.py              MFCC cosine-similarity voice pre-check
    languages.py                Fixed-phrase translations
    store.py                    In-memory demo data
tests/
  test_critical_flow.py        pytest, mirrors critical-flow.test.ts
```

## Notes specific to this implementation
- Uses the official `groq` Python SDK — same models as the TS version (`whisper-large-v3-turbo`, `openai/gpt-oss-120b`).
- BMONI calls use `httpx.AsyncClient`, matching FastAPI's async style.
- Pydantic (`models.py`) does the validation TypeScript's compiler does at build time — request bodies that don't match the shape get a 422 automatically.
- CORS is wide open (`allow_origins=["*"]`) for hackathon simplicity — tighten before this goes beyond a demo.

## Choosing between this and the TypeScript backend
Both were built, tested, and verified end-to-end (curl against every route, automated tests passing). Pick one for your actual submission and delete the other before pushing — shipping two working backends in one repo just confuses reviewers about which is "the" project. If your team is more comfortable in Python, or you want FastAPI's automatic `/docs` (Swagger UI, free from FastAPI — visit `http://localhost:4000/docs` once running) for demoing the API to judges, this is a reasonable pick over the TS version.
