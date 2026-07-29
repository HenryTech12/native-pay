import pytest

from app.models import AgentBmoniProfile
from app.services import bmoni_service, paystack_service, store
from app.services import transaction_service as ts

FAKE_RESOLVED_NAMES = {
    "0123456789": "ADEWALE OKONKWO",
    "9876543210": "NGOZI EZE",
}


async def _fake_resolve_account(account_number, bank_code):
    name = FAKE_RESOLVED_NAMES.get(account_number)
    if not name:
        raise RuntimeError("Could not resolve account")
    return {"account_number": account_number, "account_name": name, "bank_id": 1}


@pytest.fixture(autouse=True)
def mock_paystack(monkeypatch):
    """Keeps the suite offline/deterministic — no real Paystack calls in pytest."""
    monkeypatch.setattr(paystack_service, "resolve_account", _fake_resolve_account)


def test_rejects_invalid_amount():
    tx = ts.evaluate_intent("mama-aisha", "send", 0, "adewale", 0.9)
    assert tx.state == ts.STATES["INVALID_AMOUNT"]


def test_rejects_unknown_recipient():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    assert tx.state == ts.STATES["UNKNOWN_RECIPIENT"]
    assert tx.needsClarification == "accountNumber"


def test_known_recipient_gets_account_number_attached():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "adewale", 0.9)
    assert tx.recipientAccount == "0123456789"


@pytest.mark.asyncio
async def test_resolve_recipient_by_account_succeeds():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = await ts.resolve_recipient_by_account(tx.id, "0123456789", "058")
    assert resolved.state == ts.STATES["CONFIRMATION_REQUIRED"]
    assert resolved.recipient == "ADEWALE OKONKWO"
    assert resolved.recipientAccount == "0123456789"


@pytest.mark.asyncio
async def test_resolve_recipient_by_account_not_found():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = await ts.resolve_recipient_by_account(tx.id, "0000000000", "058")
    assert resolved.state == ts.STATES["UNKNOWN_RECIPIENT"]
    assert "ACCOUNT_NOT_FOUND" in (resolved.error or "")


@pytest.mark.asyncio
async def test_full_happy_path_via_account_number_resolution():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = await ts.resolve_recipient_by_account(tx.id, "9876543210", "058")
    assert resolved.state == ts.STATES["CONFIRMATION_REQUIRED"]
    ts.confirm_transaction(resolved.id)
    ts.record_face_verification(resolved.id, True)
    result = await ts.execute_transaction(resolved.id)
    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert result.recipient == "NGOZI EZE"


@pytest.mark.asyncio
async def test_resolve_recipient_respects_insufficient_funds():
    store.create_account("account-lookup-poor-user", "Poor Lookup Tester", "en")
    balance = store.get_account("account-lookup-poor-user").balance
    tx = ts.evaluate_intent("account-lookup-poor-user", "send", balance + 1000, "someone-not-in-book", 0.9)
    resolved = await ts.resolve_recipient_by_account(tx.id, "0123456789", "058")
    assert resolved.state == ts.STATES["INSUFFICIENT_FUNDS"]


def test_low_confidence_routes_to_clarification():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "adewale", 0.2)
    assert tx.state == ts.STATES["LOW_AI_CONFIDENCE"]


def test_valid_send_requires_confirmation():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    assert tx.state == ts.STATES["CONFIRMATION_REQUIRED"]


@pytest.mark.asyncio
async def test_cannot_execute_out_of_order():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    result = await ts.execute_transaction(tx.id)
    assert result.error is not None


@pytest.mark.asyncio
async def test_full_happy_path():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    result = await ts.execute_transaction(tx.id)
    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert result.bmoniReference is not None


@pytest.mark.asyncio
async def test_failed_face_verification_blocks_execution():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, False)
    result = await ts.execute_transaction(tx.id)
    assert result.error is not None


@pytest.mark.asyncio
async def test_idempotency_does_not_resend():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    first = await ts.execute_transaction(tx.id)
    second = await ts.execute_transaction(tx.id)
    assert first.bmoniReference == second.bmoniReference


def test_user_cancellation():
    tx = ts.evaluate_intent("mama-aisha", "send", 10000, "adewale", 0.95)
    cancelled = ts.cancel_transaction(tx.id)
    assert cancelled.state == ts.STATES["USER_CANCELLED"]


def test_airtime_requires_phone_number():
    tx = ts.evaluate_intent("mama-aisha", "airtime", 500, None, 0.9)
    assert tx.state == ts.STATES["UNKNOWN_RECIPIENT"]
    assert tx.needsClarification == "recipient"


@pytest.mark.asyncio
async def test_deposit_credits_balance():
    store.create_account("deposit-test-user", "Deposit Tester", "en")
    before = store.get_account("deposit-test-user").balance

    tx = ts.evaluate_intent("deposit-test-user", "deposit", 5000, None, 0.95)
    assert tx.state == ts.STATES["CONFIRMATION_REQUIRED"]
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    result = await ts.execute_transaction(tx.id)

    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert store.get_account("deposit-test-user").balance == before + 5000


@pytest.mark.asyncio
async def test_airtime_debits_balance():
    store.create_account("airtime-test-user", "Airtime Tester", "en")
    before = store.get_account("airtime-test-user").balance

    tx = ts.evaluate_intent("airtime-test-user", "airtime", 500, "08012345678", 0.95)
    assert tx.state == ts.STATES["CONFIRMATION_REQUIRED"]
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    result = await ts.execute_transaction(tx.id)

    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert store.get_account("airtime-test-user").balance == before - 500


def test_insufficient_funds_blocks_withdrawal():
    store.create_account("poor-test-user", "Poor Tester", "en")
    balance = store.get_account("poor-test-user").balance

    tx = ts.evaluate_intent("poor-test-user", "withdraw", balance + 1000, None, 0.95)
    assert tx.state == ts.STATES["INSUFFICIENT_FUNDS"]


@pytest.mark.asyncio
async def test_withdraw_uses_mock_transfer_when_agent_not_bmoni_onboarded():
    """By default the POS agent's BMONI profile isn't onboarded, so
    withdrawals keep using the generic mocked create_transfer — the real
    BMONI chain is never attempted. Customers themselves never carry
    BMONI fields at all; only the shared agent profile does."""
    store.create_account("not-onboarded-user", "Not Onboarded", "en")
    before = store.get_account("not-onboarded-user").balance

    tx = ts.evaluate_intent("not-onboarded-user", "withdraw", 3000, None, 0.95)
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    result = await ts.execute_transaction(tx.id)

    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert result.bmoniReference.startswith("NP-MOCK-")
    assert store.get_account("not-onboarded-user").balance == before - 3000


@pytest.mark.asyncio
async def test_withdraw_uses_real_bmoni_chain_when_agent_onboarded(monkeypatch):
    """Once the POS agent's shared BMONI profile is onboarded + bank-
    linked (store.update_agent_bmoni_profile), withdrawal for ANY
    customer goes through the real initiate -> sign -> submit chain
    instead of the generic mock — the agent's wallet moves the money,
    the customer's own local ledger balance is what's debited."""
    store.create_account("onboarded-flow-user", "Onboarded Flow Tester", "en")
    before = store.get_account("onboarded-flow-user").balance

    monkeypatch.setattr(store, "agent_bmoni_profile", AgentBmoniProfile(
        bmoniUserId="agent-bmoni-1", bmoniSmartWalletId="agent-wallet-1",
        bmoniWithdrawalAccountId="agent-bank-acct-1", bmoniOnboarded=True,
    ))

    calls = {}

    async def fake_initiate(user_id, source_smart_wallet_id, bank_account_id, from_amount):
        calls["initiate"] = (user_id, source_smart_wallet_id, bank_account_id, from_amount)
        return {"proposalId": "prop-1", "signPayload": {"typedData": {"fake": True}}}

    def fake_sign(sign_payload):
        calls["sign"] = sign_payload
        return "0xsignature"

    async def fake_submit(user_id, proposal_id, signature):
        calls["submit"] = (user_id, proposal_id, signature)
        return {"data": {"proposal": {"id": proposal_id, "status": "EXECUTED"}}}

    monkeypatch.setattr(bmoni_service, "initiate_nigeria_withdrawal", fake_initiate)
    monkeypatch.setattr(bmoni_service, "sign_withdrawal_payload", fake_sign)
    monkeypatch.setattr(bmoni_service, "submit_proposal_signature", fake_submit)

    tx = ts.evaluate_intent("onboarded-flow-user", "withdraw", 3000, None, 0.95)
    ts.confirm_transaction(tx.id)
    ts.record_face_verification(tx.id, True)
    result = await ts.execute_transaction(tx.id)

    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert result.bmoniReference == "prop-1"
    assert calls["initiate"] == ("agent-bmoni-1", "agent-wallet-1", "agent-bank-acct-1", "3000.00")
    assert calls["submit"] == ("agent-bmoni-1", "prop-1", "0xsignature")
    assert store.get_account("onboarded-flow-user").balance == before - 3000
