# NativePay — 3-Minute Backup Demo Video Script

Target runtime: 2:50–3:00. Record screen (browser tab on the deployed app) + your voice narrating over it. Where the *app itself* speaks (YarnGPT), let that audio play through — it's part of the proof, not something to talk over.

Default demo language below is **Yorùbá** for the voice-command segment, since it's the most fully fleshed-out phrase set in this build and reads as a genuine non-English banking interaction, not a token gesture. Swap to Pidgin/Hausa/Igbo if someone on the team speaks it more naturally on camera — the script structure doesn't change, just the spoken lines.

---

## 0:00–0:15 — Hook (presenter to camera or voice-over over a title card)

> "Millions of Nigerians can't use banking apps — not because they don't have money, but because the apps assume you can read English, own a smartphone, and remember a PIN. NativePay removes all three requirements. This is a live demo, not a mockup."

## 0:15–0:30 — One-line solution + who it's for

> "NativePay is a voice-first banking assistant for agent-run terminals — like the ATM-style kiosks already common across Nigeria. A customer walks up, inserts a card, and speaks. No reading. No app. No PIN."

*(Cut to: browser showing the virtual ATM device frame — card slot, keypad, receipt printer visible)*

## 0:30–1:50 — Live walkthrough (screen recording, ~80 seconds)

1. **Insert card** (5s) — tap "Use demo card," then "Insert card." Let the card-insert animation play.
2. **Auth** (10s) — repeat the spoken number challenge back (voice match), OR tap "Simulate: match" for the face-check fallback — whichever is faster/more reliable to record live. Say out loud for the camera: *"This voice check is a fast pre-check — face verification is the real security gate, and we say so in the app itself."*
3. **Speak a transaction** (15s) — tap the mic, say in Yorùbá: **"Mo fẹ́ yọ ẹgbẹ̀ẹ́dógún náírà"** ("I want to withdraw fifteen thousand naira"). Let Whisper transcribe it on-screen.
4. **System reads back and confirms** (10s) — let YarnGPT's Yorùbá voice speak the confirmation phrase in full before tapping "Yes, continue" — this is the fix you just shipped, so let it play out naturally, don't rush it.
5. **Face/voice verification** (10s) — tap "Simulate: match ✓" (say plainly: *"face match is simulated for the demo — disclosed, not hidden"*).
6. **Success + receipt** (10s) — let the receipt-paper animation play, YarnGPT speaks the success message, screen shows the transaction ID and reference.
7. **Quick balance check** (10s) — say "What's my balance" (or tap the quick-demo balance button) to show the balance updated correctly after the withdrawal — this proves the ledger math is real, not cosmetic.
8. **Language switch, 10s** — briefly show the language picker with all five options (English, Pidgin, Yorùbá, Hausa, Igbo) to make the inclusion point visually, even without a full second walkthrough.

## 1:50–2:25 — Technical credibility (screen recording, ~35 seconds)

*(Cut to Swagger UI or a terminal, briefly)*

> "This isn't just a UI mockup. Every piece talks to a real service."

- Flash `GET /api/health` showing `bmoniMockMode: false`.
- Flash `GET /api/agent/bmoni-status` showing a real `bmoniUserId`, `bmoniSmartWalletId`, and `bmoniOnboarded: true` — say: *"This is a real BMONI sandbox wallet — created, KYC'd, and NGN-rail-activated against their live sandbox, not simulated."*
- One sentence on the AI stack: *"Speech-to-text and intent parsing run on Groq's Whisper and LLM models; the voice you just heard is YarnGPT's Nigerian-accented text-to-speech — both real, both live."*

## 2:25–2:50 — Honesty + impact close (presenter to camera)

> "We've been upfront throughout: face verification here is simulated, and voice-matching is a heuristic pre-check, not certified biometrics — real money movement is always gated by the stronger check. What's real is the full transaction pipeline, the BMONI sandbox integration, and a genuine attempt to make banking accessible to someone who's never held a smartphone. That's NativePay."

## 2:50–3:00 — Card / call to action

> "NativePay — banking in your language, at a terminal you already know how to use."

*(End card: repo link + team name)*

---

## Recording notes

- Do the walkthrough in ONE continuous take if possible — a live, unedited flow is more convincing for a "backup" video than a heavily cut one.
- Have the app already deployed and warmed up (hit `/api/health` once before recording) so there's no cold-start lag on camera.
- If BMONI's bank-verification sandbox is still blocked when you record, skip that specific sub-step — the onboarding/KYC/wallet proof above doesn't depend on it.
- Keep a phone timer visible off-camera; if you're running long, cut the balance-check step (1:50–2:00) first — it's the least load-bearing for the judging criteria.
