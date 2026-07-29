import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerAccount, registerVoice, voiceProcess } from "../lib/api";
import { recordAudio, blobToMfccVector } from "../lib/audio";
import { generateChallenge } from "../lib/challenge";
import { phrase, speak, prefetchSpeech, LANGUAGES } from "../lib/phrases";
import DeviceFrame from "../components/DeviceFrame";
import SpeakingIndicator from "../components/SpeakingIndicator";
import { useIsSpeaking } from "../lib/useIsSpeaking";

type Step = "start" | "name" | "address" | "voiceprint" | "review" | "done";

function averageVectors(vectors: number[][]): number[] {
  const dim = vectors[0].length;
  const sum = new Array(dim).fill(0);
  vectors.forEach((v) => v.forEach((val, i) => (sum[i] += val)));
  return sum.map((v) => v / vectors.length);
}

export default function Onboarding() {
  const navigate = useNavigate();
  const isSpeaking = useIsSpeaking();
  const [step, setStep] = useState<Step>("start");
  const [langIdx, setLangIdx] = useState(0);
  const [userId, setUserId] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [status, setStatus] = useState("");
  const [submitError, setSubmitError] = useState("");

  const [fullName, setFullName] = useState("");
  const [address, setAddress] = useState("");
  const [voiceSamples, setVoiceSamples] = useState<number[][]>([]);
  const [voiceRound, setVoiceRound] = useState(1);
  const [challenge, setChallenge] = useState<{ digits: string; spoken: string } | null>(null);
  const [cardNumber, setCardNumber] = useState("");

  const recorderRef = useRef<{ stop: () => void; result: Promise<Blob> } | null>(null);
  const lang = LANGUAGES[langIdx].code;

  useEffect(() => {
    // Fetch the "name" prompt's audio as soon as a language is picked on
    // the "start" step — by the time the user taps Continue and lands on
    // "name", it's already in hand instead of starting the network
    // round-trip only once that screen appears.
    if (step === "start") prefetchSpeech(phrase(lang, "askFullName"), lang);
  }, [step, lang]);

  useEffect(() => {
    if (step === "name") {
      speak(phrase(lang, "askFullName"), lang);
      prefetchSpeech(phrase(lang, "askAddress"), lang); // next step, fetched one step ahead
    }
    if (step === "address") speak(phrase(lang, "askAddress"), lang);
  }, [step]);

  useEffect(() => {
    if (step === "voiceprint") {
      const c = generateChallenge(lang);
      setChallenge(c);
      speak(phrase(lang, "askRepeatDigits", c.spoken), lang);
    }
  }, [step, voiceRound]);

  async function captureTranscript(onDone: (text: string) => void) {
    if (isRecording) { recorderRef.current?.stop(); return; }
    setIsRecording(true);
    setStatus("Listening... tap again to stop.");
    const rec = await recordAudio();
    recorderRef.current = rec;
    rec.result.then(async (blob) => {
      setIsRecording(false);
      setStatus("Transcribing...");
      try {
        const { text } = await voiceProcess(blob, lang);
        setStatus("");
        onDone(text);
      } catch {
        setStatus("Couldn't reach the backend — check it's running and try again.");
      }
    });
  }

  async function captureVoiceprintSample() {
    if (isRecording) { recorderRef.current?.stop(); return; }
    setIsRecording(true);
    setStatus("Listening... tap again to stop.");
    const rec = await recordAudio();
    recorderRef.current = rec;
    rec.result.then(async (blob) => {
      setIsRecording(false);
      setStatus("Processing your voice sample...");
      const vector = await blobToMfccVector(blob);
      if (!vector) { setStatus("Couldn't read that clip — try again."); return; }
      const samples = [...voiceSamples, vector];
      setVoiceSamples(samples);
      setStatus("");
      if (voiceRound < 2) setVoiceRound(voiceRound + 1);
      else setStep("review");
    });
  }

  async function submit() {
    setSubmitError("");
    setStatus("Creating your account...");
    try {
      const account = await registerAccount({ userId, fullName, address, language: lang });
      setCardNumber(account.cardNumber || "");
      await registerVoice(userId, averageVectors(voiceSamples));
      await speak(phrase(lang, "enrollmentComplete"), lang);
      setStatus("");
      setStep("done");
    } catch (err) {
      setStatus("");
      setSubmitError(err instanceof Error ? err.message : "Couldn't reach the backend — check it's running and try again.");
    }
  }

  function onKeypadPress(key: string) {
    if (isSpeaking || step !== "start" || !/\d/.test(key)) return;
    setUserId((prev) => prev + key);
  }

  const titles: Record<Step, [string, string]> = {
    start: ["Create your account", "Pick your language and a phone number to sign in with."],
    name: ["Your name", "Say your full name — this becomes your account name."],
    address: ["Your address", "Say your home address."],
    voiceprint: [`Voice sample ${voiceRound} of 2`, "This is what NativePay recognizes you by next time."],
    review: ["Review", "Check the details before we create your account."],
    done: ["You're in", "Head to the virtual POS to start using NativePay."]
  };
  const [title, sub] = titles[step];

  return (
    <DeviceFrame onKeypadPress={onKeypadPress}>
      <div style={s.card}>
        <header style={s.header}>
          <div style={s.topRow}>
            <Link to="/" style={s.backLink}>← NativePay</Link>
          </div>
          <h1 style={s.h1}>{title}</h1>
          <p style={s.sub}>{sub}</p>
        </header>

        <main style={s.main}>
          <SpeakingIndicator />
          {isSpeaking && <div style={s.speakingBlock} aria-hidden="true" />}
          {step === "start" && (
            <>
              <label style={s.label}>Phone number</label>
              <input style={s.input} value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="e.g. 08012345678" />
              <div style={s.langRow}>
                {LANGUAGES.map((l, i) => (
                  <div key={l.code + i} style={{ ...s.langChip, ...(i === langIdx ? s.langChipActive : {}) }} onClick={() => setLangIdx(i)}>{l.label}</div>
                ))}
              </div>
              <button style={{ ...s.btn, ...s.btnPrimary, width: "100%" }} disabled={!userId.trim()} onClick={() => setStep("name")}>Continue</button>
            </>
          )}

          {step === "name" && (
            <div style={s.micStage}>
              <div style={s.hint}>{phrase(lang, "askFullName")}</div>
              <span style={s.linkText} onClick={() => speak(phrase(lang, "askFullName"), lang)}>🔊 Repeat prompt</span>
              <button style={{ ...s.micBtn, ...(isRecording ? s.micBtnRecording : {}) }} onClick={() => captureTranscript((text) => { setFullName(text); setStep("address"); })}>🎤</button>
              <div style={s.transcript}>{fullName || " "}</div>
              <div style={s.hint}>{status}</div>
            </div>
          )}

          {step === "address" && (
            <div style={s.micStage}>
              <div style={s.hint}>{phrase(lang, "askAddress")}</div>
              <span style={s.linkText} onClick={() => speak(phrase(lang, "askAddress"), lang)}>🔊 Repeat prompt</span>
              <button style={{ ...s.micBtn, ...(isRecording ? s.micBtnRecording : {}) }} onClick={() => captureTranscript((text) => { setAddress(text); setStep("voiceprint"); })}>🎤</button>
              <div style={s.transcript}>{address || " "}</div>
              <div style={s.hint}>{status}</div>
            </div>
          )}

          {step === "voiceprint" && challenge && (
            <div style={s.micStage}>
              <div style={s.transcript}>{challenge.spoken}</div>
              <div style={s.hint}>Listen, then tap and repeat these numbers back.</div>
              <span style={s.linkText} onClick={() => speak(phrase(lang, "askRepeatDigits", challenge.spoken), lang)}>🔊 Repeat prompt</span>
              <button style={{ ...s.micBtn, ...(isRecording ? s.micBtnRecording : {}) }} onClick={captureVoiceprintSample}>🎤</button>
              <div style={s.hint}>{status}</div>
            </div>
          )}

          {step === "review" && (
            <>
              <div style={s.reviewCard}>
                <Row label="Language" value={LANGUAGES[langIdx].label} />
                <Row label="Phone number" value={userId} />
                <Row label="Name" value={fullName} />
                <Row label="Address" value={address} />
                <Row label="Voice samples" value={`${voiceSamples.length} of 2 captured ✓`} />
              </div>
              <div style={s.mockNote}>Face verification happens live at the agent for each transaction — no photo is captured or stored during sign-up.</div>
              {submitError && <div style={s.errorCard}>{submitError}</div>}
              <button style={{ ...s.btn, ...s.btnPrimary, width: "100%", marginTop: 14 }} onClick={submit}>{status || "Create account"}</button>
            </>
          )}

          {step === "done" && (
            <>
              <div style={s.reviewCard}>
                <div style={{ textAlign: "center", fontSize: 15, color: "var(--indigo)", fontWeight: 600, marginBottom: 10 }}>✓ {fullName}, your account is ready.</div>
                {cardNumber && (
                  <div style={{ textAlign: "center" }}>
                    <div style={{ fontSize: 11, color: "#8a8175", textTransform: "uppercase", letterSpacing: "0.05em" }}>Your virtual card</div>
                    <div style={{ fontFamily: "monospace", fontSize: 17, color: "var(--charcoal)", letterSpacing: "0.05em" }}>{cardNumber}</div>
                  </div>
                )}
              </div>
              <div style={s.mockNote}>Insert this card number at the virtual POS to sign in — no need to remember your phone number.</div>
              <button style={{ ...s.btn, ...s.btnPrimary, width: "100%", marginTop: 14 }} onClick={() => navigate("/app")}>Go to virtual POS</button>
            </>
          )}
        </main>
      </div>
    </DeviceFrame>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={s.reviewRow}>
      <span style={s.reviewLabel}>{label}</span>
      <span style={s.reviewValue}>{value}</span>
    </div>
  );
}

const s: Record<string, React.CSSProperties> = {
  card: { width: "100%", maxWidth: 460, background: "#fff", borderRadius: 22, overflow: "hidden", boxShadow: "0 20px 60px rgba(19,28,59,0.18)", border: "1px solid var(--line)" },
  header: { background: "var(--indigo)", color: "var(--paper)", padding: "20px 26px 16px" },
  topRow: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 },
  backLink: { color: "var(--gold-light)", fontSize: 12, textDecoration: "none" },
  h1: { fontFamily: "Fraunces, serif", fontWeight: 700, fontSize: 21, margin: "0 0 4px" },
  sub: { margin: 0, fontSize: 12, color: "rgba(245,239,226,0.75)" },
  main: { padding: "24px 26px", minHeight: 340, display: "flex", flexDirection: "column", position: "relative" },
  speakingBlock: { position: "absolute", inset: 0, zIndex: 5, cursor: "not-allowed", background: "transparent" },
  label: { fontSize: 13, fontWeight: 600, color: "#5c5346", marginBottom: 6, display: "block" },
  input: { width: "100%", padding: "12px 14px", borderRadius: 10, border: "1px solid var(--line)", fontSize: 15, marginBottom: 14 },
  langRow: { display: "flex", gap: 7, marginBottom: 20, flexWrap: "wrap" },
  langChip: { border: "1px solid var(--line)", background: "#fff", padding: "6px 11px", borderRadius: 100, fontSize: 12, fontWeight: 600, cursor: "pointer" },
  langChipActive: { background: "var(--indigo)", color: "#fff", borderColor: "var(--indigo)" },
  linkText: { color: "var(--indigo)", fontWeight: 700, cursor: "pointer", textDecoration: "underline", fontSize: 12 },
  micStage: { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", flex: 1, gap: 14, padding: "4px 0" },
  micBtn: { width: 88, height: 88, borderRadius: "50%", border: "none", background: "var(--gold)", color: "#fff", fontSize: 30, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 8px 24px rgba(201,138,44,0.35)" },
  micBtnRecording: { background: "var(--alert)" },
  hint: { fontSize: "12.5px", color: "#6b6357", textAlign: "center", maxWidth: 300 },
  transcript: { fontFamily: "Fraunces, serif", fontSize: "16.5px", textAlign: "center", color: "var(--indigo)", minHeight: 24, padding: "0 8px" },
  btn: { padding: 13, borderRadius: 12, border: "none", fontWeight: 700, fontSize: "14.5px", cursor: "pointer" },
  btnPrimary: { background: "var(--indigo)", color: "#fff" },
  reviewCard: { background: "var(--paper)", border: "1px solid var(--line)", borderRadius: 14, padding: 18 },
  reviewRow: { display: "flex", justifyContent: "space-between", fontSize: 13, padding: "6px 0", borderBottom: "1px dashed var(--line)" },
  reviewLabel: { color: "#8a8175" },
  reviewValue: { fontWeight: 600, color: "var(--charcoal)" },
  mockNote: { fontSize: "10.5px", color: "#a08a5f", background: "#fbf3e2", border: "1px dashed #d9b978", padding: "8px 10px", borderRadius: 8, textAlign: "center", marginTop: 14 },
  errorCard: { background: "#fdf1ef", border: "1px solid #f0c7be", borderRadius: 14, padding: 14, textAlign: "center", color: "var(--alert)", fontSize: 13, marginTop: 12 }
};
