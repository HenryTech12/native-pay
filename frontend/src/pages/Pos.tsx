import { useState } from "react";
import { getTransaction } from "../lib/api";
import type { TransactionRecord } from "../types";

function stateClass(state: string): "ok" | "err" | "pending" {
  if (state === "TRANSACTION_SUCCESS") return "ok";
  if (["TRANSACTION_FAILED", "FACE_VERIFICATION_FAILED", "BMONI_API_ERROR", "INVALID_AMOUNT", "UNKNOWN_RECIPIENT", "USER_CANCELLED"].includes(state)) return "err";
  return "pending";
}

const badgeColors = { ok: "#3D7A5C", err: "#B23A2E", pending: "#C98A2C" };

export default function Pos() {
  const [txId, setTxId] = useState("");
  const [tx, setTx] = useState<TransactionRecord | null>(null);
  const [notFound, setNotFound] = useState(false);

  async function lookup() {
    setNotFound(false);
    setTx(null);
    if (!txId.trim()) return;
    try {
      const result = await getTransaction(txId.trim());
      setTx(result);
    } catch {
      setNotFound(true);
    }
  }

  return (
    <div style={{ minHeight: "100vh", padding: 24, fontFamily: "Inter, sans-serif", color: "#241F1A" }}>
      <div style={{ maxWidth: 640, margin: "0 auto" }}>
        <h1 style={{ fontFamily: "Fraunces, serif", color: "#1E2A52", fontSize: 24 }}>NativePay — POS Agent View</h1>
        <p style={{ fontSize: 13, color: "#6b6357", marginBottom: 20 }}>
          Track a customer's transaction status here. The agent never sees the customer's transcript, biometric data, or account credentials — only status.
        </p>

        <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
          <input
            value={txId}
            onChange={(e) => setTxId(e.target.value)}
            placeholder="Transaction ID (e.g. NP-2026-123456)"
            style={{ flex: 1, padding: 12, borderRadius: 10, border: "1px solid rgba(36,31,26,0.14)", fontSize: 14 }}
          />
          <button onClick={lookup} style={{ padding: "12px 18px", borderRadius: 10, border: "none", background: "#1E2A52", color: "#fff", fontWeight: 700, cursor: "pointer" }}>
            Look up
          </button>
        </div>

        {notFound && <div style={{ color: "#8a8175", fontSize: "13.5px", textAlign: "center", padding: "30px 0" }}>No transaction found — check the ID, or the backend may not be reachable.</div>}

        {tx && (
          <>
            <Card label="Status">
              <span style={{ display: "inline-block", fontSize: 11, fontWeight: 700, padding: "4px 10px", borderRadius: 100, color: "#fff", background: badgeColors[stateClass(tx.state)] }}>
                {tx.state.replace(/_/g, " ")}
              </span>
            </Card>
            <Card label="Type">{tx.action === "send" ? "Send money" : tx.action === "withdraw" ? "Withdraw cash" : "Balance check"}</Card>
            <Card label="Amount">{tx.amount ? `₦${tx.amount.toLocaleString()}` : "—"}</Card>
            <Card label="Face verification">{tx.faceVerified ? "✓ Verified" : "Not yet verified"}</Card>
            <Card label="Started">{new Date(tx.createdAt).toLocaleString()}</Card>
          </>
        )}

        <div style={{ fontSize: "11.5px", color: "#a08a5f", background: "#fbf3e2", border: "1px dashed #d9b978", padding: "8px 12px", borderRadius: 8, marginTop: 20 }}>
          Demo/sandbox mode. This view is read-only status — it facilitates the session, it does not control the customer's account.
        </div>
      </div>
    </div>
  );
}

function Card({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "#fff", border: "1px solid rgba(36,31,26,0.14)", borderRadius: 14, padding: 18, marginBottom: 14 }}>
      <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "0.05em", color: "#8a8175", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 16, fontWeight: 600 }}>{children}</div>
    </div>
  );
}
