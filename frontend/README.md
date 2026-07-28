# NativePay Frontend

React + TypeScript + Vite client for NativePay — the voice UI, the enrollment wizard, the virtual POS, and the agent status view.

## Setup
```bash
npm install
cp .env.example .env   # VITE_API_BASE=http://localhost:4000
npm run dev
```
Requires the backend running (see `../backend/README.md`) — most pages call it directly and don't work standalone. Browser microphone/camera permissions are required for voice and face steps.

## Scripts
- `npm run dev` — dev server
- `npm run build` — typecheck (`tsc -b`) then production build
- `npm run lint` — oxlint
- `npm run preview` — preview a production build

## Routes
| Path | Page | Purpose |
|---|---|---|
| `/` | `Landing.tsx` | Marketing/pitch page |
| `/onboarding` | `Onboarding.tsx` | Sign-up wizard: language → name → address → voiceprint → review |
| `/app` | `App.tsx` | The virtual POS: session login (voice/face) → speak a request → confirm → face verify → receipt |
| `/pos` | `Pos.tsx` | Read-only agent view — transaction status lookup by ID, no customer data |
| `/history` | `History.tsx` | Transaction history for the demo account |

## Structure
```
src/
  lib/
    api.ts          Every backend call, one function per route
    audio.ts        getUserMedia recording + Meyda MFCC feature extraction
    challenge.ts     Random-digit spoken challenge generator (anti-replay, client-side)
    phrases.ts       Per-language spoken/display strings + speechSynthesis wrapper
  pages/
    Landing.tsx, Onboarding.tsx, App.tsx, Pos.tsx, History.tsx
  types.ts          Shared types — mirrors backend/app/models.py
```

## Key flows

**Enrollment** (`Onboarding.tsx`): pick a language, speak full name and address (transcribed via `/api/voice/process`), record two voice samples prompted by a random-digit challenge (`generateChallenge`), average their MFCC vectors, then `POST /api/accounts/register` + `POST /api/voice/register`.

**Session auth** (`App.tsx`, `start`/`auth`/`faceAuth`/`authFailed` steps): enter a phone number; if a voiceprint exists, a fresh random-digit challenge is spoken and recorded, checked via `POST /api/voice/authorize`. A confident match skips straight into the app; a low-confidence match or no enrollment at all steps up to a simulated face check.

**Transaction** (`listen`/`confirm`/`face`/`processing`/`receipt` steps): speak or pick a quick-demo intent, confirm the read-back amount/recipient, pass a (simulated) face check, then the backend executes against BMONI (mock) and a receipt is shown.

## Honest limitations
- Face match is simulated (tap "match"/"no match") — flagged on-screen wherever it appears, not hidden.
- Voice auth (`authorizeVoice`) is a cosine-similarity pre-check on the backend, not verified speaker biometrics; the random digit challenge (`challenge.ts`) is a client-side UX device against replay — the backend does not check that the spoken content matches the digits.
- Yorùbá/Hausa/Igbo/Pidgin strings in `phrases.ts` are best-effort translations, not reviewed by native speakers.
