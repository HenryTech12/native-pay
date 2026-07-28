"""
In-memory store for the hackathon demo — deliberately not a real DB.
Every other module talks only to these functions, never to storage directly,
so swapping this for real persistence later doesn't touch calling code.
"""

import random
from datetime import datetime, timezone
from typing import Optional

from app.models import Account, Recipient, TransactionRecord

accounts: dict[str, Account] = {
    "mama-aisha": Account(id="mama-aisha", name="Mama Aisha", preferredLanguage="yo", balance=85000)
}

recipients: dict[str, Recipient] = {
    "adewale": Recipient(name="Adewale", account="0123456789"),
    "ngozi": Recipient(name="Ngozi", account="9876543210"),
    "ibrahim": Recipient(name="Ibrahim", account="1234567890"),
}

transactions: dict[str, TransactionRecord] = {}


def create_transaction_record(
    user_id: str,
    action: str,
    amount: Optional[int],
    recipient: Optional[str],
    confidence: Optional[float],
) -> TransactionRecord:
    tx_id = f"NP-{datetime.now(timezone.utc).year}-{random.randint(100000, 999999)}"
    record = TransactionRecord(
        id=tx_id,
        userId=user_id,
        action=action,
        amount=amount,
        recipient=recipient,
        confidence=confidence,
        state="INTENT_DETECTED",
        createdAt=datetime.now(timezone.utc).isoformat(),
        faceVerified=False,
        bmoniReference=None,
        error=None,
    )
    transactions[tx_id] = record
    return record


STARTING_BALANCE = 50000


def create_account(user_id: str, name: str, preferred_language: str, address: Optional[str] = None) -> Account:
    account = Account(
        id=user_id,
        name=name,
        preferredLanguage=preferred_language,
        balance=STARTING_BALANCE,
        address=address,
    )
    accounts[user_id] = account
    return account


def get_account(user_id: str) -> Optional[Account]:
    return accounts.get(user_id)


def get_transaction(tx_id: str) -> Optional[TransactionRecord]:
    return transactions.get(tx_id)


def update_transaction(tx_id: str, **patch) -> Optional[TransactionRecord]:
    existing = transactions.get(tx_id)
    if not existing:
        return None
    updated = existing.model_copy(update=patch)
    transactions[tx_id] = updated
    return updated


def list_transactions(user_id: Optional[str] = None) -> list[TransactionRecord]:
    all_tx = list(transactions.values())
    if user_id:
        all_tx = [t for t in all_tx if t.userId == user_id]
    return sorted(all_tx, key=lambda t: t.createdAt, reverse=True)
