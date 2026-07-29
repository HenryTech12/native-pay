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
    "mama-aisha": Account(
        id="mama-aisha", name="Mama Aisha", preferredLanguage="yo", balance=85000,
        cardNumber="5060 0000 0000 0001",
    )
}

accounts_by_card: dict[str, str] = {"5060000000000001": "mama-aisha"}

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


def _normalize_card(card_number: str) -> str:
    return card_number.replace(" ", "").replace("-", "")


def _generate_card_number() -> str:
    while True:
        digits = "".join(str(random.randint(0, 9)) for _ in range(12))
        normalized = "5060" + digits
        if normalized not in accounts_by_card:
            return " ".join(normalized[i:i + 4] for i in range(0, 16, 4))


def create_account(user_id: str, name: str, preferred_language: str, address: Optional[str] = None) -> Account:
    card_number = _generate_card_number()
    account = Account(
        id=user_id,
        name=name,
        preferredLanguage=preferred_language,
        balance=STARTING_BALANCE,
        address=address,
        cardNumber=card_number,
    )
    accounts[user_id] = account
    accounts_by_card[_normalize_card(card_number)] = user_id
    return account


def get_account(user_id: str) -> Optional[Account]:
    return accounts.get(user_id)


def adjust_balance(user_id: str, delta: int) -> Optional[Account]:
    account = accounts.get(user_id)
    if not account:
        return None
    updated = account.model_copy(update={"balance": account.balance + delta})
    accounts[user_id] = updated
    return updated


def get_account_by_card(card_number: str) -> Optional[Account]:
    user_id = accounts_by_card.get(_normalize_card(card_number))
    return accounts.get(user_id) if user_id else None


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
