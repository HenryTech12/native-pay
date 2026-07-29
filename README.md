# NativePay Backend

FastAPI service backing the NativePay frontend: speech-to-text + intent parsing, the transaction state machine, voice-based auth, and account enrollment. In-memory storage, sandbox-mode BMONI — built for the NITHUB Innovation Fair Hackathon 2026, not production.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in GROQ_API_KEY at minimum
uvicorn app.main:app --reload --port 4000
```
Runs on `http://localhost:4000`. Visit `http://localhost:4000/docs` for the auto-generated Swagger UI.

## Tests
```bash
python -m pytest tests/ -v
```
(Run as `python -m pytest`, not bare `pytest` — the module needs the repo root on `sys.path`.)

9 cases in `tests/test_critical_flow.py`: invalid amount, unknown recipient, low-confidence clarification, blocked out-of-order execution, the confirm→face-verify→send→success happy path, idempotency, and cancellation.

## API reference

### Voice & language
| Route | Method | Purpose |
|---|---|---|
| `/api/voice/process` | POST | Transcribe audio (multipart `audio` + optional `language`) and parse it into an intent |
| `/api/transcribe` | POST | Transcribe only, no intent parsing |
| `/api/ai/intent` | POST | Parse intent from raw text |
| `/api/voice/register` | POST | Store a voiceprint (`userId`, `featureVector`) — overwrites any existing one |
| `/api/voice/authorize` | POST | Compare a feature vector against the stored voiceprint; returns `{authorized, similarity, threshold}` |
| `/api/voice/status/{userId}` | GET | Whether a voiceprint is on file for this user |
| `/api/languages` | GET | Supported language codes/labels |

### Accounts
| Route | Method | Purpose |
|---|---|---|
| `/api/accounts/register` | POST | Create an account (`userId`, `fullName`, `address`, `language`) — 409 if the userId already exists |
| `/api/accounts/{id}` | GET | Fetch an account profile |
| `/api/accounts/{id}/balance` | GET | Balance lookup — falls back to the seeded demo account if `id` isn't found |

### Transactions
| Route | Method | Purpose |
|---|---|---|
| `/api/transactions/confirm` | POST | Two shapes: no `id` → evaluate a new intent into a transaction; `id` present → advance `CONFIRMATION_REQUIRED` → `FACE_VERIFICATION_REQUIRED` |
| `/api/transactions/verify-face` | POST | Record the (simulated) face-match result for a transaction |
| `/api/transactions/send` | POST | Execute a `FACE_VERIFIED` transaction against BMONI (mock); idempotent |
| `/api/transactions/{id}/cancel` | POST | Cancel a transaction |
| `/api/transactions` | GET | List transactions, optional `?userId=` filter |
| `/api/transactions/{id}` | GET | Fetch one transaction |
| `/api/transactions/{id}/receipt` | GET | Receipt for a `TRANSACTION_SUCCESS` transaction |

### BMONI onboarding + withdrawal (real sandbox, per BMONI's OpenAPI reference)
Self-custodied smart-wallet flow: create user → create wallet (owner-proof challenge + EIP-191 signature) → KYC (profile PATCH + SumSub activation) → activate NGN rail → read wallet/balance/transactions → withdraw to a real Nigerian bank account (offramp proposal + EIP-712 signature). Runs in mock mode until `BMONI_API_KEY`/`BMONI_OWNER_PRIVATE_KEY` are set.
| Route | Method | Purpose |
|---|---|---|
| `/api/bmoni/generate-owner-wallet` | POST | One-time: generates the EVM keypair that signs every user's owner-proof challenge and withdrawal proposals |
| `/api/bmoni/users` | POST | Create a BMONI sandbox user (optionally with a BVN to auto-fill profile fields) |
| `/api/bmoni/users/{id}/wallet` | POST | Owner-proof challenge → sign (EIP-191) → create managed smart wallet |
| `/api/bmoni/users/{id}/kyc` | POST | PATCH the KYC profile (BVN) then activate it for SumSub review |
| `/api/bmoni/users/{id}/onboarding-status` | GET | Check onboarding status across providers |
| `/api/bmoni/users/{id}/activate-nigeria` | POST | Activate the NGN rail |
| `/api/bmoni/users/{id}/wallets` | GET | Real wallet list |
| `/api/bmoni/users/{id}/real-balances` | GET | Real wallet balances |
| `/api/bmoni/users/{id}/wallets/{smartWalletId}/real-transactions` | GET | Real wallet transaction history |
| `/api/bmoni/users/{id}/nigerian-banks` | GET | Supported banks + CBN codes for withdrawal |
| `/api/bmoni/users/{id}/verify-nigerian-account` | POST | Name-enquiry on a Nigerian account number before creating a withdrawal account |
| `/api/bmoni/users/{id}/withdrawal-account` | POST | Register the payout bank account a withdrawal settles to |
| `/api/bmoni/users/{id}/withdraw-nigeria` | POST | Full real withdrawal round trip: creates the offramp proposal, signs the EIP-712 payload, submits the signature — the one BMONI-powered financial function that actually moves money in this demo |

There's no BMONI endpoint for arbitrary P2P "send" or an NGN-only deposit (only card/crypto deposit exist), so this app's send/deposit/airtime actions keep using its own balance bookkeeping — matching the quick-start doc's note that sandbox wallets are funded manually by BMONI staff, not via API.

### Health
`/api/health` — `{ok, demoMode, bmoniMockMode}`

## Structure
```
app/
  main.py                    FastAPI routes
  models.py                  Pydantic models (mirrors frontend/src/types.ts)
  services/
    groq_service.py            Whisper STT (speech-in) + LLM intent parsing
    yarngpt_service.py         YarnGPT TTS (speech-out) — Nigerian-accented read-back voice
    paystack_service.py       Real bank account name-enquiry (recipient resolution)
    bmoni_service.py           Real BMONI sandbox integration (mock fallback)
    transaction_service.py     State machine, server-side validation
    voice_auth.py              MFCC cosine-similarity voice pre-check
    languages.py                Fixed-phrase translations
    store.py                    In-memory demo data (accounts, recipients, transactions)
tests/
  test_critical_flow.py        pytest
```

## Notes
- Voice is two separate real integrations, not one: **Whisper** (via the official `groq` SDK, `whisper-large-v3-turbo`) transcribes what the user says (speech-in); **YarnGPT** synthesizes the Nigerian-accented voice that reads confirmations/balances back (speech-out). Requires real `GROQ_API_KEY` / `YARNGPT_API_KEY` respectively — without them, `/api/voice/process` or `/api/tts` fail (the frontend falls back to `speechSynthesis` for TTS, and surfaces STT failures as a network error rather than crashing).
- `openai/gpt-oss-120b` (also via Groq) does intent parsing from the transcribed text.
- BMONI calls use `httpx.AsyncClient` against the real sandbox (`x-api-key` auth, no `/v1` appended to the base URL) once `BMONI_API_KEY`/`BMONI_OWNER_PRIVATE_KEY` are set; `bmoniMockMode` in `/api/health` reflects that. The self-custodied wallet's owner-proof challenge is signed with `eth_account` (EIP-191), and Nigeria bank withdrawals are signed with EIP-712 typed data — both since this backend has no Flutter/React Native SDK access. P2P send and NGN deposit have no corresponding BMONI endpoint, so those stay on this app's own balance bookkeeping.
- Pydantic (`models.py`) validates request bodies — malformed shapes get a 422 automatically.
- CORS is wide open (`allow_origins=["*"]`) for hackathon simplicity — tighten before this goes beyond a demo.
- `voice_auth.py` is a heuristic pre-check (cosine similarity over MFCC vectors), not trained speaker-verification. Face capture is the real authorization gate; voice only decides whether a session skips straight to it.
- Storage (`store.py`) is process-memory only — restarting the server clears every account, voiceprint, and transaction.
- Supported `action` values: `send`, `withdraw`, `deposit`, `airtime`, `balance` (`bill` is defined in the type but not implemented anywhere — treat it as unsupported). Send/withdraw/airtime debit the account's balance and require an amount that doesn't exceed it (`INSUFFICIENT_FUNDS` otherwise); deposit credits it. `airtime` uses `recipient` to hold the phone number being topped up, not a contact name — it isn't checked against the recipient book the way `send` is.
