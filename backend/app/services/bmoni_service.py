"""
BMONIService interface — createTransfer / getTransactionStatus /
getAccountBalance / generateReceipt, matching the shape used by the
TS backend so either can sit behind the same frontend.

Mock mode runs automatically whenever BMONI_API_KEY is unset, generating
realistic reference IDs so the rest of the app is fully testable before
real sandbox access is confirmed. Flip to live calls by setting real
credentials in .env — no route or frontend code changes needed.
"""

import asyncio
import os
import random
import time
from typing import Optional

import httpx

from app.models import TransactionRecord

BASE_URL = os.environ.get("BMONI_BASE_URL")
API_KEY = os.environ.get("BMONI_API_KEY")

MOCK_MODE = not API_KEY or API_KEY == "your_bmoni_sandbox_key_here"


def _mock_reference() -> str:
    return f"NP-MOCK-{int(time.time() * 1000)}-{random.randint(0, 9999)}"


def is_mock_mode() -> bool:
    return MOCK_MODE


async def create_transfer(amount: Optional[int], recipient: Optional[str]) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(1.0)
        return {
            "status": "success",
            "reference": _mock_reference(),
            "amount": amount,
            "recipient": recipient,
            "environment": "sandbox-mock",
        }
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{BASE_URL}/transfers",
            json={"amount": amount, "recipient": recipient, "test_mode": True},
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI transfer failed ({res.status_code}): {res.text}")
        return res.json()


async def get_transaction_status(reference: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.25)
        return {"status": "confirmed", "reference": reference, "environment": "sandbox-mock"}
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/transfers/{reference}", headers={"Authorization": f"Bearer {API_KEY}"})
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI status check failed ({res.status_code}): {res.text}")
        return res.json()


async def get_account_balance(account_id: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.2)
        return {"accountId": account_id, "balance": 85000, "currency": "NGN", "environment": "sandbox-mock"}
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/accounts/{account_id}/balance", headers={"Authorization": f"Bearer {API_KEY}"})
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI balance lookup failed ({res.status_code}): {res.text}")
        return res.json()


def generate_receipt(tx: TransactionRecord) -> dict:
    return {
        "transactionId": tx.id,
        "type": tx.action,
        "amount": tx.amount,
        "recipient": tx.recipient,
        "reference": tx.bmoniReference,
        "status": tx.state,
        "date": tx.createdAt,
        "environment": "sandbox-mock" if MOCK_MODE else "sandbox-live",
    }
