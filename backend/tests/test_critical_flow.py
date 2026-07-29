import pytest

from app.services import store
from app.services import transaction_service as ts


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


def test_resolve_recipient_by_account_succeeds():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = ts.resolve_recipient_by_account(tx.id, "0123456789")
    assert resolved.state == ts.STATES["CONFIRMATION_REQUIRED"]
    assert resolved.recipient == "adewale"
    assert resolved.recipientAccount == "0123456789"


def test_resolve_recipient_by_account_not_found():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = ts.resolve_recipient_by_account(tx.id, "0000000000")
    assert resolved.state == ts.STATES["UNKNOWN_RECIPIENT"]
    assert resolved.error == "ACCOUNT_NOT_FOUND"


@pytest.mark.asyncio
async def test_full_happy_path_via_account_number_resolution():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    resolved = ts.resolve_recipient_by_account(tx.id, "9876543210")
    assert resolved.state == ts.STATES["CONFIRMATION_REQUIRED"]
    ts.confirm_transaction(resolved.id)
    ts.record_face_verification(resolved.id, True)
    result = await ts.execute_transaction(resolved.id)
    assert result.state == ts.STATES["TRANSACTION_SUCCESS"]
    assert result.recipient == "ngozi"


def test_resolve_recipient_respects_insufficient_funds():
    store.create_account("account-lookup-poor-user", "Poor Lookup Tester", "en")
    balance = store.get_account("account-lookup-poor-user").balance
    tx = ts.evaluate_intent("account-lookup-poor-user", "send", balance + 1000, "someone-not-in-book", 0.9)
    resolved = ts.resolve_recipient_by_account(tx.id, "1234567890")
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
