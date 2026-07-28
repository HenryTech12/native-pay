"""
Explicit state machine. The AI only ever proposes an intent — every
transition is decided and validated here, server-side, never by the LLM
output directly. Mirrors transactionService.ts exactly so either backend
produces identical transaction behavior against the same frontend.
"""

from typing import Optional

from app.models import TransactionRecord
from app.services import store
from app.services.bmoni_service import create_transfer

STATES = {
    "INTENT_DETECTED": "INTENT_DETECTED",
    "COLLECTING_DETAILS": "COLLECTING_DETAILS",
    "CONFIRMATION_REQUIRED": "CONFIRMATION_REQUIRED",
    "USER_CONFIRMED": "USER_CONFIRMED",
    "FACE_VERIFICATION_REQUIRED": "FACE_VERIFICATION_REQUIRED",
    "FACE_VERIFIED": "FACE_VERIFIED",
    "TRANSACTION_PROCESSING": "TRANSACTION_PROCESSING",
    "TRANSACTION_SUCCESS": "TRANSACTION_SUCCESS",
    "USER_CANCELLED": "USER_CANCELLED",
    "INVALID_AMOUNT": "INVALID_AMOUNT",
    "UNKNOWN_RECIPIENT": "UNKNOWN_RECIPIENT",
    "LOW_AI_CONFIDENCE": "LOW_AI_CONFIDENCE",
    "TRANSACTION_FAILED": "TRANSACTION_FAILED",
    "FACE_VERIFICATION_FAILED": "FACE_VERIFICATION_FAILED",
    "BMONI_API_ERROR": "BMONI_API_ERROR",
}

LOW_CONFIDENCE_THRESHOLD = 0.55


def evaluate_intent(
    user_id: str,
    action: str,
    amount: Optional[int],
    recipient: Optional[str],
    confidence: Optional[float],
) -> TransactionRecord:
    if (confidence if confidence is not None else 1) < LOW_CONFIDENCE_THRESHOLD:
        record = store.create_transaction_record(user_id, action, amount, recipient, confidence)
        return store.update_transaction(record.id, state=STATES["LOW_AI_CONFIDENCE"], needsClarification="recipient")

    if action in ("send", "withdraw"):
        if not amount or amount <= 0:
            record = store.create_transaction_record(user_id, action, amount, recipient, confidence)
            return store.update_transaction(record.id, state=STATES["INVALID_AMOUNT"])

    if action == "send":
        key = (recipient or "").lower().strip()
        if not key or key not in store.recipients:
            record = store.create_transaction_record(user_id, action, amount, recipient, confidence)
            return store.update_transaction(record.id, state=STATES["UNKNOWN_RECIPIENT"])

    record = store.create_transaction_record(user_id, action, amount, recipient, confidence)
    next_state = STATES["TRANSACTION_PROCESSING"] if action == "balance" else STATES["CONFIRMATION_REQUIRED"]
    return store.update_transaction(record.id, state=next_state)


def confirm_transaction(tx_id: str) -> Optional[TransactionRecord]:
    tx = store.get_transaction(tx_id)
    if not tx:
        return None
    if tx.state != STATES["CONFIRMATION_REQUIRED"]:
        return tx.model_copy(update={"error": f"Cannot confirm from state {tx.state}"})
    return store.update_transaction(tx_id, state=STATES["FACE_VERIFICATION_REQUIRED"])


def cancel_transaction(tx_id: str) -> Optional[TransactionRecord]:
    tx = store.get_transaction(tx_id)
    if not tx:
        return None
    return store.update_transaction(tx_id, state=STATES["USER_CANCELLED"])


def record_face_verification(tx_id: str, matched: bool) -> Optional[TransactionRecord]:
    tx = store.get_transaction(tx_id)
    if not tx:
        return None
    if not matched:
        return store.update_transaction(tx_id, state=STATES["FACE_VERIFICATION_FAILED"])
    return store.update_transaction(tx_id, state=STATES["FACE_VERIFIED"], faceVerified=True)


async def execute_transaction(tx_id: str) -> Optional[TransactionRecord]:
    """Idempotent: calling this twice for the same transactionId never double-sends."""
    tx = store.get_transaction(tx_id)
    if not tx:
        return None

    if tx.state == STATES["TRANSACTION_SUCCESS"]:
        return tx  # already executed — return the existing result, don't resend
    if tx.state != STATES["FACE_VERIFIED"]:
        return tx.model_copy(update={"error": f"Cannot execute from state {tx.state}"})

    store.update_transaction(tx_id, state=STATES["TRANSACTION_PROCESSING"])

    try:
        if tx.action in ("send", "withdraw"):
            result = await create_transfer(tx.amount, tx.recipient or "self (withdrawal)")
            return store.update_transaction(tx_id, state=STATES["TRANSACTION_SUCCESS"], bmoniReference=result["reference"])
        return store.update_transaction(tx_id, state=STATES["TRANSACTION_SUCCESS"])
    except Exception as err:
        return store.update_transaction(tx_id, state=STATES["BMONI_API_ERROR"], error=str(err))


def get_account_balance(user_id: str) -> Optional[int]:
    account = store.accounts.get(user_id) or store.accounts.get("mama-aisha")
    return account.balance if account else None
