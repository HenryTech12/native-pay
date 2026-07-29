# NativePay

Voice-first banking for people the app-based banking model leaves out — built for the **NITHUB Innovation Fair Hackathon 2026**.

## The problem

Nigeria's agent-banking networks (OPay, PalmPay, Moniepoint) already solved *physical* access to financial services — there's an agent within reach of most people. What's still locked out is the *interaction layer*: an app UI in English, PINs to remember, menus to read. Nigeria has 500+ languages; English is official but not most people's first language, especially older adults, rural traders, and market women. Roughly 30–36% of Nigerian adults remain financially excluded or under-served (EFInA/CBN), and a meaningful share of that is a literacy/language barrier on top of infrastructure that already reaches them.

NativePay replaces the app UI with a conversation. Speak in English, Nigerian Pidgin, Yorùbá, Hausa, or Igbo, at a participating agent's terminal — no reading, no PIN.

## How it works

1. **Enroll once** — pick a language, say your name and address (transcribed), and record two short voice samples used as your voiceprint.
2. **Speak naturally** — "Send ten thousand naira to Adewale" — transcribed and parsed into an intent (amount, recipient, action).
3. **Confirm out loud** — NativePay reads the transaction back before anything moves.
4. **Verify it's you** — a fresh random-digit challenge is spoken and repeated back each session; a voiceprint match lets you straight in, a low-confidence match or no enrollment steps up to a face check.
5. **BMONI executes** it — send, withdraw, deposit, airtime top-up, or a balance check — and a spoken + digital receipt confirms it. Send/withdraw/airtime/deposit all move the account's real (in-memory) balance; an insufficient-funds check blocks send/withdraw/airtime before confirmation if the amount exceeds it.

## Architecture

```
native-pay/
  frontend/    React + TypeScript + Vite client — the voice UI, the virtual POS, the agent status view
  backend/     FastAPI service — speech-to-text, intent parsing, the transaction state machine, voice auth
```

The two talk over HTTP; the frontend expects the backend at `http://localhost:4000` by default (`frontend/.env`'s `VITE_API_BASE`). See `frontend/README.md` and `backend/README.md` for setup and endpoint details on each side.

## Identity & auth model

Two independent checks, not one:

- **Voice** is the fast path in. A fresh random-digit challenge is generated and spoken each session — never the enrollment phrase, so a recording overheard once can't be replayed. The backend compares an MFCC feature vector against the one captured at enrollment (cosine similarity, no external biometrics vendor).
- **Face** is the actual authorization gate for money movement, and also the fallback whenever voice isn't confident enough (below the similarity threshold, or the phone number was never enrolled). Every send/withdraw still requires a face check regardless of how the session started — voice only decides whether you skip straight to it.

This is a deliberate two-tier design: voice for a low-friction session start, face as the harder gate before funds move.

## Quickstart

**Backend** (see `backend/README.md` for details):
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY
uvicorn app.main:app --reload --port 4000
```

**Frontend** (see `frontend/README.md` for details):
```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE=http://localhost:4000
npm run dev
```

Then open the printed local URL. Key routes: `/` (landing), `/onboarding` (sign up), `/app` (virtual POS), `/pos` (agent status view), `/history`.

## Honest limitations (sandbox/demo mode)

- **Face verification is simulated** in the UI (tap "match" / "no match") — no real facial-recognition vendor is wired in. This is stated on-screen wherever it appears.
- **BMONI runs in mock mode** by default — no real money moves.
- **Storage is in-memory** on the backend — restarting it clears all accounts and transactions.
- **Yorùbá/Hausa/Igbo/Pidgin translations** are best-effort, not reviewed by native speakers — sanity-check before a live pitch if you have access to one.
- **Voice matching is a heuristic pre-check** (MFCC cosine similarity), not trained speaker-verification — reasonable for a hackathon demo, not a production biometric claim.

## Tests

```bash
cd backend && python -m pytest tests/ -v   # 9 cases: validation, the confirm→face→send→success happy path, idempotency, cancellation
cd frontend && npx tsc -b && npm run build # typecheck + production build
```
