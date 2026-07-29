"""
BMONI sandbox integration, per BMONI's hackathon quick-start doc:

    Create user -> Create wallet -> Complete KYC -> Activate NGN rail ->
    Fund wallet -> Read or move money

Mock mode runs automatically whenever BMONI_API_KEY is unset, so the rest
of the app stays testable before real sandbox access is confirmed.

Wallets are self-custodied: BMONI expects an owner keypair whose address
signs a server-issued challenge message. The quick-start doc points teams
at BMONI's Flutter/React Native SDK to do that signing, but this backend
is plain Python/FastAPI, so signing is done here with eth_account instead
(standard EIP-191 personal-sign — verification is address recovery via
ecrecover, so it doesn't matter which library produced the signature).

Several field names below (the challenge response shape, the
create-managed-wallet body, the KYC submission endpoint) are inferred
from the quick-start doc's partial examples, not the full interactive API
reference (embedded-dev.bmoni.com/docs) — expect to need small corrections
once this runs against the live sandbox for the first time.
"""

import asyncio
import os
import random
import time
from typing import Optional

import httpx
from eth_account import Account
from eth_account.messages import encode_defunct

from app.models import TransactionRecord

BASE_URL = os.environ.get("BMONI_BASE_URL") or "https://embedded-dev.bmoni.com"
API_KEY = os.environ.get("BMONI_API_KEY")
OWNER_PRIVATE_KEY = os.environ.get("BMONI_OWNER_PRIVATE_KEY")

MOCK_MODE = not API_KEY or API_KEY == "your_bmoni_sandbox_key_here"

SANDBOX_TEST_BVN = "22222222222"
SANDBOX_COUNTRY_CODE = "NGA"


def _headers() -> dict:
    return {"x-api-key": API_KEY or "", "Content-Type": "application/json"}


def _mock_reference() -> str:
    return f"NP-MOCK-{int(time.time() * 1000)}-{random.randint(0, 9999)}"


def is_mock_mode() -> bool:
    return MOCK_MODE


def generate_owner_wallet() -> dict:
    """One-time setup helper — generates a fresh EVM keypair for the
    self-custodied smart-wallet owner. Save the privateKey as
    BMONI_OWNER_PRIVATE_KEY in .env; every onboarded user in this demo
    reuses that one owner key."""
    acct = Account.create()
    return {"address": acct.address, "privateKey": acct.key.hex()}


def _owner_account() -> Account:
    if not OWNER_PRIVATE_KEY:
        raise RuntimeError(
            "BMONI_OWNER_PRIVATE_KEY not set — call generate_owner_wallet() once "
            "and save the returned privateKey to .env"
        )
    return Account.from_key(OWNER_PRIVATE_KEY)


async def create_user(first_name: str, email: str, phone_number: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.2)
        return {"bmoniUserId": f"mock-user-{random.randint(100000, 999999)}", "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.post("/v1/users", json={
            "firstName": first_name, "email": email, "phoneNumber": phone_number,
        })
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI create_user failed ({res.status_code}): {res.text}")
        return res.json()


async def create_smart_wallet(user_id: str) -> dict:
    """Requests an owner-proof challenge, signs it with our owner keypair,
    then creates the managed smart wallet. CNGN per the quick-start doc's
    note: use CNGN, not NGN, for the wallet currency."""
    if MOCK_MODE:
        await asyncio.sleep(0.2)
        return {"smartWalletId": f"mock-wallet-{random.randint(100000, 999999)}", "address": "0xMOCK", "environment": "sandbox-mock"}

    owner = _owner_account()
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        challenge_res = await client.post(
            f"/v1/users/{user_id}/smart-wallets/owner-proof-challenges",
            json={"currency": "CNGN", "userOwnerAddress": owner.address},
        )
        if challenge_res.status_code >= 400:
            raise RuntimeError(f"BMONI owner-proof-challenge failed ({challenge_res.status_code}): {challenge_res.text}")
        challenge = challenge_res.json()

        challenge_id = challenge.get("challengeId") or challenge.get("id")
        message = challenge.get("message") or challenge.get("challenge")
        if not message:
            raise RuntimeError(f"BMONI owner-proof-challenge response had no signable message field: {challenge}")

        signed = Account.sign_message(encode_defunct(text=message), private_key=owner.key)

        create_res = await client.post(
            f"/v1/users/{user_id}/smart-wallets/create-managed",
            json={
                "challengeId": challenge_id,
                "signature": signed.signature.hex(),
                "ownerAddress": owner.address,
            },
        )
        if create_res.status_code >= 400:
            raise RuntimeError(f"BMONI create-managed-wallet failed ({create_res.status_code}): {create_res.text}")
        return create_res.json()


async def submit_kyc(user_id: str, bvn: str = SANDBOX_TEST_BVN, country_code: str = SANDBOX_COUNTRY_CODE) -> dict:
    """Endpoint path/body inferred — the quick-start doc only documents the
    status-check GET, not the submission POST. Verify against
    embedded-dev.bmoni.com/docs before relying on this in the live demo."""
    if MOCK_MODE:
        await asyncio.sleep(0.2)
        return {"status": "pending", "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.post(f"/v1/users/{user_id}/onboarding/kyc", json={
            "bvn": bvn, "countryCode": country_code,
        })
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI submit_kyc failed ({res.status_code}): {res.text}")
        return res.json()


async def get_onboarding_status(user_id: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        return {"status": "active", "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.get(f"/v1/users/{user_id}/onboarding/status")
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI onboarding status check failed ({res.status_code}): {res.text}")
        return res.json()


async def activate_nigeria_rail(user_id: str, wallet_address: str, wallet_index: int = 0, bvn: str = SANDBOX_TEST_BVN) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.2)
        return {"status": "active", "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.post(f"/v1/users/{user_id}/onboarding/start-nigeria", json={
            "bvn": bvn, "walletAddress": wallet_address, "walletIndex": wallet_index,
        })
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI start-nigeria failed ({res.status_code}): {res.text}")
        return res.json()


async def get_wallets(user_id: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        return {"wallets": [], "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.get(f"/v1/users/{user_id}/smart-wallets/account/wallets")
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI get_wallets failed ({res.status_code}): {res.text}")
        return res.json()


async def get_real_balances(user_id: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        return {"balances": [], "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.get(f"/v1/users/{user_id}/smart-wallets/account/balances")
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI get_balances failed ({res.status_code}): {res.text}")
        return res.json()


async def get_real_transactions(user_id: str) -> dict:
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        return {"transactions": [], "environment": "sandbox-mock"}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers()) as client:
        res = await client.get(f"/v1/users/{user_id}/smart-wallets/account/transactions")
        if res.status_code >= 400:
            raise RuntimeError(f"BMONI get_transactions failed ({res.status_code}): {res.text}")
        return res.json()


async def create_transfer(amount: Optional[int], recipient: Optional[str]) -> dict:
    """Money-movement endpoint isn't specified in the hackathon quick-start
    doc (only user/wallet/KYC/rail/read endpoints are). Stays mocked until
    the real withdrawal/fund endpoint shape is confirmed from BMONI's
    interactive docs or their staff — real reads (balance/transactions
    above) already hit the live sandbox once onboarding is real."""
    await asyncio.sleep(1.0)
    return {
        "status": "success",
        "reference": _mock_reference(),
        "amount": amount,
        "recipient": recipient,
        "environment": "sandbox-mock",
    }


async def get_transaction_status(reference: str) -> dict:
    await asyncio.sleep(0.25)
    return {"status": "confirmed", "reference": reference, "environment": "sandbox-mock"}


async def get_account_balance(account_id: str) -> dict:
    await asyncio.sleep(0.2)
    return {"accountId": account_id, "balance": 300000, "currency": "NGN", "environment": "sandbox-mock"}


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
