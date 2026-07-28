import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listTransactions } from "../lib/api";
import type { TransactionRecord } from "../types";

function stateColor(state: string): string {
  if (state === "TRANSACTION_SUCCESS") return "#3D7A5C";
  if (["TRANSACTION_FAILED", "FACE_VERIFICATION_FAILED", "BMONI_API_ERROR", "INVALID_AMOUNT", "UNKNOWN_RECIPIENT", "USER_CANCELLED"].includes(state)) return "#B23A2E";
  return "#C98A2C";
}

function actionLabel(action: string): string {
  return { send: "Sent", withdraw: "Withdrew", balance: "Balance check" }[action] || action;
}

export default function History() {
  const [txs, setTxs] = useState<TransactionRecord[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    listTransactions("mama-aisha")
      .then(setTxs)
      .catch(() => setError(true));
  }, []);

  return (
    <div style={{ minHeight: "100vh", padding: 24, fontFamily: "Inter, sans-serif", color: "#241F1A" }}>
      <div style={{ maxWidth: 560, margin: "0 auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
          <h1 style={{ fontFamily: "Fraunces, serif", color: "#1E2A52", fontSize: 24, margin: 0 }}>Transaction history</h1>
          <Link to="/app" style={{ fontSize: 13, color: "#1E2A52", fontWeight: 600, textDecoration: "none" }}>← Back to app</Link>
        </div>

        {error && <div style={{ color: "#8a8175", fontSize: "13.5px", textAlign: "center", padding: "30px 0" }}>Couldn't reach the NativePay backend. Check it's running.</div>}
        {!error && txs === null && <div style={{ color: "#8a8175", fontSize: "13.5px", textAlign: "center", padding: "30px 0" }}>Loading...</div>}
        {txs && txs.length === 0 && <div style={{ color: "#8a8175", fontSize: "13.5px", textAlign: "center", padding: "30px 0" }}>No transactions yet — try the demo.</div>}

        {txs && txs.map((tx) => (
          <div key={tx.id} style={{ background: "#fff", border: "1px solid rgba(36,31,26,0.14)", borderRadius: 14, padding: 16, marginBottom: 10, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: 14.5 }}>
                {actionLabel(tx.action)}{tx.amount ? ` ₦${tx.amount.toLocaleString()}` : ""}{tx.recipient ? ` to ${tx.recipient}` : ""}
              </div>
              <div style={{ fontSize: 12, color: "#8a8175", marginTop: 2 }}>{tx.id} · {new Date(tx.createdAt).toLocaleString()}</div>
            </div>
            <span style={{ fontSize: 10, fontWeight: 700, padding: "4px 9px", borderRadius: 100, color: "#fff", background: stateColor(tx.state), whiteSpace: "nowrap" }}>
              {tx.state.replace(/_/g, " ")}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
