import type {
  Action, AccountProfile, AccountRegisterPayload, Bank, ParsedIntent, Receipt,
  TransactionRecord, VoiceAuthorizeResult, VoiceStatus
} from "../types";

export const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:4000";

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = res.statusText;
    try {
      const body = await res.json();
      message = body.message || body.error || message;
    } catch {
      /* body wasn't JSON — keep statusText */
    }
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}

export async function synthesizeSpeech(text: string, language: string): Promise<Blob> {
  const res = await fetch(`${API_BASE}/api/tts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language })
  });
  if (!res.ok) throw new Error("TTS_UNAVAILABLE");
  return res.blob();
}

export async function voiceProcess(blob: Blob, languageCode?: string): Promise<{ text: string; intent: ParsedIntent }> {
  const form = new FormData();
  form.append("audio", blob, "clip.webm");
  if (languageCode && languageCode !== "pcm") form.append("language", languageCode);
  const res = await fetch(`${API_BASE}/api/voice/process`, { method: "POST", body: form });
  return asJson(res);
}

export async function confirmCreate(
  userId: string, action: Action, amount: number | null, recipient: string | null, confidence: number | null
): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, action, amount, recipient, confidence })
  });
  return asJson(res);
}

export async function confirmAdvance(id: string, voiceFeatureVector?: number[] | null): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, voiceFeatureVector: voiceFeatureVector || undefined })
  });
  return asJson(res);
}

export async function cancelTransaction(id: string): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/${id}/cancel`, { method: "POST" });
  return asJson(res);
}

export async function resolveRecipientByAccount(id: string, accountNumber: string, bankCode: string): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/resolve-recipient`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, accountNumber, bankCode })
  });
  return asJson(res);
}

export async function getBanks(): Promise<Bank[]> {
  const res = await fetch(`${API_BASE}/api/banks`);
  return asJson(res);
}

export async function verifyFace(id: string, matched: boolean): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/verify-face`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, matched })
  });
  return asJson(res);
}

export async function sendTransaction(id: string): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/send`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
  return asJson(res);
}

export async function getReceipt(id: string): Promise<Receipt> {
  const res = await fetch(`${API_BASE}/api/transactions/${id}/receipt`);
  return asJson(res);
}

export async function getBalance(userId: string): Promise<{ accountId: string; balance: number; currency: string }> {
  const res = await fetch(`${API_BASE}/api/accounts/${userId}/balance`);
  return asJson(res);
}

export async function registerVoice(userId: string, featureVector: number[]): Promise<{ registered: boolean }> {
  const res = await fetch(`${API_BASE}/api/voice/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, featureVector })
  });
  return asJson(res);
}

export async function authorizeVoice(userId: string, featureVector: number[]): Promise<VoiceAuthorizeResult> {
  const res = await fetch(`${API_BASE}/api/voice/authorize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, featureVector })
  });
  return asJson(res);
}

export async function getVoiceStatus(userId: string): Promise<VoiceStatus> {
  const res = await fetch(`${API_BASE}/api/voice/status/${encodeURIComponent(userId)}`);
  return asJson(res);
}

export async function registerAccount(payload: AccountRegisterPayload): Promise<AccountProfile> {
  const res = await fetch(`${API_BASE}/api/accounts/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return asJson(res);
}

export async function getAccount(userId: string): Promise<AccountProfile> {
  const res = await fetch(`${API_BASE}/api/accounts/${encodeURIComponent(userId)}`);
  return asJson(res);
}

export async function getAccountByCard(cardNumber: string): Promise<AccountProfile> {
  const res = await fetch(`${API_BASE}/api/accounts/by-card/${encodeURIComponent(cardNumber)}`);
  return asJson(res);
}

export async function getTransaction(id: string): Promise<TransactionRecord> {
  const res = await fetch(`${API_BASE}/api/transactions/${id}`);
  return asJson(res);
}

export async function listTransactions(userId?: string): Promise<TransactionRecord[]> {
  const url = userId ? `${API_BASE}/api/transactions?userId=${encodeURIComponent(userId)}` : `${API_BASE}/api/transactions`;
  const res = await fetch(url);
  return asJson(res);
}
