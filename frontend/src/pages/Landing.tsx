import { Link } from "react-router-dom";

const styles: Record<string, React.CSSProperties> = {
  nav: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "22px 6vw", position: "sticky", top: 0, background: "rgba(245,239,226,0.9)", backdropFilter: "blur(8px)", zIndex: 10, borderBottom: "1px solid var(--line)" },
  logo: { fontFamily: "Fraunces, serif", fontWeight: 700, fontSize: 20, color: "var(--indigo)" },
  navLinks: { display: "flex", alignItems: "center", gap: 14 },
  posLink: { fontSize: 13, color: "var(--indigo)", textDecoration: "none", fontWeight: 600 },
  cta: { background: "var(--indigo)", color: "var(--paper)", padding: "10px 20px", borderRadius: 100, textDecoration: "none", fontWeight: 600, fontSize: 14 },
  hero: { display: "flex", alignItems: "center", gap: 60, padding: "8vh 6vw 10vh", maxWidth: 1200, margin: "0 auto", flexWrap: "wrap" },
  heroText: { flex: 1, minWidth: 320 },
  eyebrow: { display: "inline-flex", alignItems: "center", gap: 8, fontSize: "12.5px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--gold)", marginBottom: 18 },
  h1: { fontFamily: "Fraunces, serif", fontWeight: 700, fontSize: "clamp(34px, 5vw, 54px)", lineHeight: 1.08, color: "var(--indigo)", marginBottom: 20, letterSpacing: "-0.01em" },
  em: { fontStyle: "normal", color: "var(--gold)" },
  lede: { fontSize: 17, lineHeight: 1.6, color: "#4a4238", maxWidth: 480, marginBottom: 30 },
  heroCtas: { display: "flex", gap: 14, flexWrap: "wrap" },
  btnPrimary: { background: "var(--gold)", color: "#fff", padding: "15px 28px", borderRadius: 12, textDecoration: "none", fontWeight: 700, fontSize: 15, boxShadow: "0 8px 20px rgba(201,138,44,.3)" },
  btnSecondary: { background: "transparent", color: "var(--indigo)", padding: "15px 28px", borderRadius: 12, textDecoration: "none", fontWeight: 700, fontSize: 15, border: "1.5px solid var(--indigo)" },
  heroDemo: { flex: 1, minWidth: 280, maxWidth: 340, background: "var(--indigo)", borderRadius: 24, padding: 30, color: "var(--paper)", position: "relative", overflow: "hidden" },
  phraseYo: { fontFamily: "Fraunces, serif", fontSize: 19, marginBottom: 6 },
  phraseEn: { fontSize: "13.5px", color: "rgba(245,239,226,.65)", marginBottom: 22 },
  demoReceipt: { background: "rgba(245,239,226,.08)", border: "1px solid rgba(245,239,226,.18)", borderRadius: 14, padding: 16, fontSize: "13.5px" },
  receiptRow: { display: "flex", justifyContent: "space-between", padding: "4px 0" },
  ok: { color: "var(--gold-light)", fontWeight: 700 },
  section: { padding: "6vh 6vw 10vh", maxWidth: 1200, margin: "0 auto" },
  sectionAlt: { padding: "8vh 6vw", background: "var(--indigo-deep)" },
  sectionAltInner: { maxWidth: 1200, margin: "0 auto" },
  sectionHead: { maxWidth: 560, marginBottom: 44 },
  h2: { fontFamily: "Fraunces, serif", fontSize: 30, color: "var(--indigo)", marginBottom: 10 },
  h2Light: { fontFamily: "Fraunces, serif", fontSize: 30, color: "var(--paper)", marginBottom: 10 },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))", gap: 22 },
  card: { background: "#fff", border: "1px solid var(--line)", borderRadius: 16, padding: 24 },
  cardNum: { fontFamily: "Fraunces, serif", fontSize: 13, color: "var(--gold)", fontWeight: 700, marginBottom: 10 },
  cardH3: { fontSize: "16.5px", marginBottom: 8, color: "var(--indigo)" },
  cardP: { fontSize: "13.5px", color: "#5c5346", lineHeight: 1.55 },
  problemGrid: { display: "flex", gap: 40, flexWrap: "wrap", alignItems: "flex-start" },
  statBlock: { flex: "1 1 340px", minWidth: 300, display: "flex", gap: 24, flexWrap: "wrap" },
  stat: { flex: "1 1 140px" },
  statNum: { fontFamily: "Fraunces, serif", fontSize: 40, fontWeight: 700, color: "var(--gold)", lineHeight: 1 },
  statLabel: { fontSize: "12.5px", color: "#4a4238", marginTop: 8, lineHeight: 1.4 },
  statSource: { fontSize: 11, color: "#8a8175", marginTop: 4 },
  personaBlock: { flex: "1 1 340px", minWidth: 300, background: "#fff", border: "1px solid var(--line)", borderRadius: 16, padding: 26 },
  personaQuote: { fontFamily: "Fraunces, serif", fontStyle: "italic", fontSize: 16, color: "var(--indigo)", lineHeight: 1.5, marginBottom: 10 },
  personaAttr: { fontSize: 12, color: "#8a8175" },
  trustGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 18, marginTop: 30 },
  trustCard: { background: "rgba(245,239,226,0.06)", border: "1px solid rgba(245,239,226,0.15)", borderRadius: 14, padding: 20 },
  trustH3: { fontSize: 14.5, color: "var(--gold-light)", fontWeight: 700, marginBottom: 6 },
  trustP: { fontSize: 13, color: "rgba(245,239,226,0.75)", lineHeight: 1.5 },
  honestyNote: { marginTop: 30, fontSize: 12.5, color: "rgba(245,239,226,0.55)", lineHeight: 1.6, maxWidth: 720 },
  footer: { padding: "5vh 6vw", textAlign: "center", color: "#8a8175", fontSize: 13, borderTop: "1px solid var(--line)" }
};

const features = [
  { num: "01", title: "Speak", body: "Say what you want in your own language. Groq's speech AI transcribes it in under a second." },
  { num: "02", title: "Confirm", body: "NativePay reads the transaction back to you out loud before anything moves." },
  { num: "03", title: "Verify", body: "A quick face check replaces PINs and passwords — nothing to remember, nothing to forget." },
  { num: "04", title: "Done", body: "BMONI processes the transfer and NativePay confirms it out loud, with a digital receipt." }
];

export default function Landing() {
  return (
    <div>
      <nav style={styles.nav}>
        <div style={styles.logo}>NativePay</div>
        <div style={styles.navLinks}>
          <Link to="/pos" style={styles.posLink}>POS agent view</Link>
          <Link to="/onboarding" style={styles.posLink}>Onboard a customer</Link>
          <Link to="/app" style={styles.cta}>Try the demo</Link>
        </div>
      </nav>

      <div style={styles.hero}>
        <div style={styles.heroText}>
          <div style={styles.eyebrow}>NITHUB Innovation Fair 2026 · AI + BMONI</div>
          <h1 style={styles.h1}>Banking that speaks <span style={styles.em}>your</span> language.</h1>
          <p style={styles.lede}>No apps to learn. No PINs to forget. Walk up to any participating POS agent, speak naturally in Yorùbá, Hausa, Igbo, or Pidgin, and NativePay handles the rest — securely, through BMONI.</p>
          <div style={styles.heroCtas}>
            <Link to="/app" style={styles.btnPrimary}>Start speaking</Link>
            <a href="#problem" style={styles.btnSecondary}>Why we built this</a>
          </div>
        </div>
        <div style={styles.heroDemo}>
          <div style={styles.phraseYo}>"Mo fẹ́ fi ẹgbẹ̀rún mẹ́wàá ránṣẹ́ sí ọmọ mi."</div>
          <div style={styles.phraseEn}>"I want to send ₦10,000 to my daughter."</div>
          <div style={styles.demoReceipt}>
            <div style={styles.receiptRow}><span>Amount</span><span>₦10,000</span></div>
            <div style={styles.receiptRow}><span>To</span><span>Adaeze</span></div>
            <div style={styles.receiptRow}><span>Status</span><span style={styles.ok}>✓ Sent</span></div>
          </div>
        </div>
      </div>

      <section style={styles.section} id="problem">
        <div style={styles.sectionHead}>
          <h2 style={styles.h2}>The problem isn't money. It's the interface.</h2>
          <p style={{ color: "#4a4238", fontSize: 15, lineHeight: 1.6 }}>Nigeria's digital banking push has left a specific group behind — and it's not because they can't afford an account.</p>
        </div>
        <div style={styles.problemGrid}>
          <div style={styles.statBlock}>
            <div style={styles.stat}>
              <div style={styles.statNum}>~36%</div>
              <div style={styles.statLabel}>of Nigerian adults remain unbanked</div>
              <div style={styles.statSource}>World Bank, via Techpoint Africa</div>
            </div>
            <div style={styles.stat}>
              <div style={styles.statNum}>26%</div>
              <div style={styles.statLabel}>of Nigerians are financially excluded — down from 32% in 2020, but still tens of millions of people</div>
              <div style={styles.statSource}>EFInA Access to Finance survey, 2023</div>
            </div>
          </div>
          <div style={styles.personaBlock}>
            <div style={styles.personaQuote}>"Most elderly adults studied never adopted internet banking — they simply returned to traditional, in-person banking."</div>
            <div style={styles.personaAttr}>Digital Inclusion and the Elderly: Internet Banking Use and Non-Use among Older Adults in Ekiti State, Nigeria — Covenant University Journal of Business and Social Sciences</div>
          </div>
        </div>
      </section>

      <section style={styles.section} id="features">
        <div style={styles.sectionHead}>
          <h2 style={styles.h2}>How it works</h2>
          <p style={{ color: "#4a4238", fontSize: 15, lineHeight: 1.6 }}>Every step is designed for someone who has never used a banking app — and never needs to.</p>
        </div>
        <div style={styles.grid}>
          {features.map((f) => (
            <div style={styles.card} key={f.num}>
              <div style={styles.cardNum}>{f.num}</div>
              <h3 style={styles.cardH3}>{f.title}</h3>
              <p style={styles.cardP}>{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      <div style={styles.sectionAlt}>
        <div style={styles.sectionAltInner}>
          <h2 style={styles.h2Light}>Built on real infrastructure, not a mockup</h2>
          <p style={{ color: "rgba(245,239,226,0.7)", fontSize: 15, lineHeight: 1.6, maxWidth: 560 }}>Every service below is a live integration — you can verify each one yourself from the POS agent view.</p>
          <div style={styles.trustGrid}>
            <div style={styles.trustCard}>
              <div style={styles.trustH3}>Groq · Whisper</div>
              <div style={styles.trustP}>Real speech-to-text transcription and LLM intent parsing, tuned for Nigerian languages and Naira amounts.</div>
            </div>
            <div style={styles.trustCard}>
              <div style={styles.trustH3}>YarnGPT</div>
              <div style={styles.trustP}>Nigerian-accented text-to-speech for every confirmation, balance, and success message the system speaks.</div>
            </div>
            <div style={styles.trustCard}>
              <div style={styles.trustH3}>Paystack</div>
              <div style={styles.trustP}>Real Nigerian bank-account name-enquiry, used to verify unrecognized send recipients before any transfer.</div>
            </div>
            <div style={styles.trustCard}>
              <div style={styles.trustH3}>BMONI</div>
              <div style={styles.trustP}>Real sandbox wallet — created, KYC'd, and NGN-rail-activated — settling real withdrawals through a signed on-chain proposal.</div>
            </div>
          </div>
          <p style={styles.honestyNote}>We're upfront about the rest, too: face verification in this build is simulated, and voice-matching is a heuristic pre-check, not certified biometrics. Real money movement is always gated by the stronger check, and every transaction records exactly which one verified it.</p>
        </div>
      </div>

      <footer style={styles.footer}>NativePay — built for NITHUB Innovation Fair Hackathon 2026. Sandbox / test data only.</footer>
    </div>
  );
}
