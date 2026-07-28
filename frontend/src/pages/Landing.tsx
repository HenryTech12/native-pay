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
  sectionHead: { maxWidth: 560, marginBottom: 44 },
  h2: { fontFamily: "Fraunces, serif", fontSize: 30, color: "var(--indigo)", marginBottom: 10 },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))", gap: 22 },
  card: { background: "#fff", border: "1px solid var(--line)", borderRadius: 16, padding: 24 },
  cardNum: { fontFamily: "Fraunces, serif", fontSize: 13, color: "var(--gold)", fontWeight: 700, marginBottom: 10 },
  cardH3: { fontSize: "16.5px", marginBottom: 8, color: "var(--indigo)" },
  cardP: { fontSize: "13.5px", color: "#5c5346", lineHeight: 1.55 },
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
          <Link to="/onboarding" style={styles.posLink}>Create account</Link>
          <Link to="/app" style={styles.cta}>Try the demo</Link>
        </div>
      </nav>

      <div style={styles.hero}>
        <div style={styles.heroText}>
          <div style={styles.eyebrow}>NITHUB Innovation Fair 2026 · AI + BMONI</div>
          <h1 style={styles.h1}>Banking that speaks <span style={styles.em}>your</span> language.</h1>
          <p style={styles.lede}>No apps to learn. No PINs to forget. Walk up to any participating POS agent, speak naturally in Yoruba, Hausa, Igbo, or Pidgin, and NativePay handles the rest — securely, through BMONI.</p>
          <div style={styles.heroCtas}>
            <Link to="/app" style={styles.btnPrimary}>Start speaking</Link>
            <a href="#features" style={styles.btnSecondary}>How it works</a>
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

      <footer style={styles.footer}>NativePay — built for NITHUB Innovation Fair Hackathon 2026. Sandbox / test data only.</footer>
    </div>
  );
}
