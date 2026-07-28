import pytest

from app.services import transaction_service as ts


def test_rejects_invalid_amount():
    tx = ts.evaluate_intent("mama-aisha", "send", 0, "adewale", 0.9)
    assert tx.state == ts.STATES["INVALID_AMOUNT"]


def test_rejects_unknown_recipient():
    tx = ts.evaluate_intent("mama-aisha", "send", 5000, "someone-not-in-book", 0.9)
    assert tx.state == ts.STATES["UNKNOWN_RECIPIENT"]


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
