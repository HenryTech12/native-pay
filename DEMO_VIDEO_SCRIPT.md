# NativePay — 3-Minute Backup Demo Video Script

Target runtime: 2:50–3:00. Record screen (browser tab on the deployed app) + your voice narrating over it. Where the *app itself* speaks (YarnGPT), let that audio play through — it's part of the proof, not something to talk over.

Central persona for this cut: **an elderly Nigerian who has never used a banking app.** Every stat cited below is real and sourced (listed at the bottom) — nothing here is a guessed number.

Default demo language is **Yorùbá** for the voice-command segment, since it's the most fully fleshed-out phrase set in this build. Swap to Pidgin/Hausa/Igbo if someone on the team speaks it more naturally on camera — the structure doesn't change, just the spoken lines.

---

## 0:00–0:25 — Hook: the person, then the numbers (presenter to camera or voice-over over a title card)

> "Picture an elderly woman in Lagos. She's never opened a banking app in her life — not because she doesn't have money, but because no one designed one for her. This isn't a hypothetical. According to the World Bank, roughly 36 percent of Nigerian adults are still unbanked. EFInA's 2023 survey put financial exclusion nationwide at 26 percent — real progress from 32 percent in 2020, but tens of millions still locked out. And a Covenant University study on elderly adults in Ekiti State found something specific: most of them never adopted internet banking at all — they simply went back to traditional, in-person banking, because the digital option wasn't built with them in mind."

## 0:25–0:40 — One-line solution

> "NativePay is a voice-first banking assistant for agent-run terminals — the same ATM-style kiosks already common across Nigeria. She walks up, inserts a card, and speaks. No reading. No app. No PIN."

*(Cut to: browser showing the virtual ATM device frame — card slot, keypad, receipt printer visible)*

## 0:40–2:00 — Live walkthrough, in character (screen recording, ~80 seconds)

Narrate this as *her* interaction, not a generic feature tour — "she inserts her card," "she says," "she hears" — keep the persona present throughout.

1. **Insert card** (5s) — tap "Use demo card," then "Insert card." Let the card-insert animation play.
2. **Auth** (10s) — repeat the spoken number challenge back (voice match), or tap "Simulate: match" for the face-check fallback. Say: *"This voice check is a fast pre-check — face verification is the real security gate, and the app says so itself. Nothing here overstates what's real and what's simulated."*
3. **Speak a transaction** (15s) — tap the mic, say in Yorùbá: **"Mo fẹ́ yọ ẹgbẹ̀ẹ́dógún náírà"** ("I want to withdraw fifteen thousand naira"). Let Whisper transcribe it on-screen.
4. **System reads back and confirms** (10s) — let YarnGPT's Yorùbá voice speak the confirmation phrase in full before tapping "Yes, continue" — let it play out naturally.
5. **Face/voice verification** (10s) — tap "Simulate: match ✓" (say: *"face match is simulated for this demo — disclosed, not hidden"*).
6. **Success + receipt** (10s) — let the receipt-paper animation play, YarnGPT speaks the success message, screen shows the transaction ID and reference.
7. **Quick balance check** (10s) — say "What's my balance" (or tap the quick-demo balance button) — proves the ledger updated for real, not cosmetically.
8. **Language switch** (10s) — briefly show all five language options. Say: *"English, Pidgin, Yorùbá, Hausa, Igbo — she banks in the language she actually thinks in."*

## 2:00–2:35 — Technical credibility (screen recording, ~35 seconds)

*(Navigate to `/pos` — the POS Agent View — right within the app, no need to cut away to Swagger)*

> "This isn't a mockup. Every piece talks to a real service — and you don't have to take my word for it, it's right here in the product."

- Point at the "Agent BMONI status" panel: mode badge ("Live sandbox," not mock), "Agent onboarded: Yes," and the real (truncated) `bmoniUserId` / smart wallet ID / wallet address — say: *"This is a real BMONI sandbox wallet — created, KYC'd, and NGN-rail-activated against their live sandbox, not simulated."*
- One line on the AI stack: *"Speech-to-text and intent parsing run on Groq's Whisper and LLM models; the voice she just heard is YarnGPT's Nigerian-accented text-to-speech — both real, both live."*

## 2:35–2:55 — Honesty + impact close (presenter to camera)

> "We've been upfront throughout: face verification here is simulated, and voice-matching is a heuristic pre-check, not certified biometrics — real money movement is always gated by the stronger check. What's real is the full transaction pipeline, the BMONI sandbox integration, and a genuine attempt to close the gap that research keeps finding in Nigeria's elderly population — not through more literacy campaigns, but by removing the requirement to read at all. That's NativePay."

## 2:55–3:00 — Card / call to action

> "NativePay — banking in your language, at a terminal you already know how to use."

*(End card: repo link + team name)*

---

## Sources cited in the script (real, verified — say them naturally, no need to show URLs on screen)

- World Bank (via Techpoint Africa): ~36% of Nigerian adults unbanked — https://techpoint.africa/general/nigerian-adults-banked/
- EFInA Access to Finance (A2F) 2023 Survey: 26% financially excluded nationally (down from 32% in 2020) — https://efina.org.ng/wp-content/uploads/2024/03/A2F-2023-Event-Day-Presentation-Version4-1.pdf
- "Digital Inclusion and the Elderly: The Case of Internet Banking Use and Non-Use among older Adults in Ekiti State, Nigeria" (Covenant University Journal of Business and Social Sciences) — https://www.researchgate.net/publication/344858260_Digital_Inclusion_and_the_Elderly_The_Case_of_Internet_Banking_Use_and_Non-Use_among_older_Adults_in_Ekiti_State_Nigeria

If a judge asks "where's that stat from" during Q&A, you have a real, named source for every number in this script — say it, don't hedge.

## Recording notes

- Do the walkthrough in ONE continuous take if possible — a live, unedited flow is more convincing for a "backup" video than a heavily cut one.
- Have the app already deployed and warmed up (hit `/api/health` once before recording) so there's no cold-start lag on camera.
- If BMONI's bank-verification sandbox is still blocked when you record, skip that specific sub-step — the onboarding/KYC/wallet proof above doesn't depend on it.
- Keep a phone timer visible off-camera; if you're running long, cut the balance-check step first — it's the least load-bearing for the judging criteria.
- Practice the hook (0:00–0:25) out loud once before recording — it's the densest part with three cited stats back to back, and it needs to sound natural, not read off a page.
