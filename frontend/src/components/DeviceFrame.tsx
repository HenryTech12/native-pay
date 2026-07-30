import type { ReactNode } from "react";

interface DeviceFrameProps {
  children: ReactNode;
  showReceiptPrint?: boolean;
  cardSlotActive?: boolean;
  onKeypadPress?: (key: string) => void;
}

export default function DeviceFrame({ children, showReceiptPrint, cardSlotActive, onKeypadPress }: DeviceFrameProps) {
  return (
    <div style={s.body}>
      <div style={s.deviceChassis}>
        <div style={s.deviceTopRow}>
          <div style={{ ...s.cardSlot, ...(cardSlotActive ? s.cardSlotActive : {}) }} title="Card slot" />
          <div style={s.brandPlaque}>ElderPay <span style={s.modelTag}>EP-100</span></div>
          <div style={s.statusIcons}>●●●</div>
        </div>
        <div style={s.printerSlot}>
          {showReceiptPrint && <div style={s.receiptPaper} />}
        </div>

        <div style={s.screenBezel}>{children}</div>

        <div style={s.keypad}>
          {["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"].map((k) => (
            <button key={k} style={s.keypadKey} onClick={() => onKeypadPress?.(k)}>{k}</button>
          ))}
        </div>
        <div style={s.speakerGrille}>
          {Array.from({ length: 10 }).map((_, i) => <span key={i} style={s.speakerDot} />)}
        </div>
      </div>
    </div>
  );
}

const s: Record<string, React.CSSProperties> = {
  body: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 },
  deviceChassis: { width: "100%", maxWidth: 520, background: "linear-gradient(160deg, #2b2f38 0%, #1a1d23 100%)", borderRadius: 34, padding: "20px 22px 26px", boxShadow: "0 30px 70px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.08)" },
  deviceTopRow: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10, padding: "0 4px" },
  cardSlot: { width: 46, height: 6, borderRadius: 3, background: "#0d0f13", boxShadow: "inset 0 1px 3px rgba(0,0,0,0.8)" },
  cardSlotActive: { animation: "slotGlow 550ms ease-in-out" },
  brandPlaque: { fontSize: 11, fontWeight: 700, letterSpacing: "0.06em", color: "rgba(245,239,226,0.55)", textTransform: "uppercase" },
  modelTag: { color: "rgba(245,239,226,0.3)", fontWeight: 500, marginLeft: 4, textTransform: "none" },
  statusIcons: { fontSize: 8, color: "rgba(245,239,226,0.35)", letterSpacing: 2 },
  printerSlot: { height: 10, borderRadius: 5, background: "#0d0f13", boxShadow: "inset 0 2px 4px rgba(0,0,0,0.8)", marginBottom: 16, position: "relative" },
  receiptPaper: { position: "absolute", top: "100%", left: "50%", width: 120, height: 46, background: "#fdfbf5", borderRadius: "2px 2px 6px 6px", boxShadow: "0 6px 14px rgba(0,0,0,0.3)", animation: "printOut 900ms ease-out forwards" },
  screenBezel: { background: "#0d0f13", borderRadius: 26, padding: 10, boxShadow: "inset 0 2px 8px rgba(0,0,0,0.6)" },
  keypad: { display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10, marginTop: 18, padding: "0 10px" },
  keypadKey: { padding: "12px 0", borderRadius: 10, border: "none", background: "linear-gradient(180deg, #3a3f4a, #262a32)", color: "rgba(245,239,226,0.85)", fontSize: 15, fontWeight: 700, cursor: "pointer", boxShadow: "0 2px 0 rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08)" },
  speakerGrille: { display: "flex", justifyContent: "center", gap: 4, marginTop: 14 },
  speakerDot: { width: 3, height: 3, borderRadius: "50%", background: "rgba(245,239,226,0.15)" }
};
