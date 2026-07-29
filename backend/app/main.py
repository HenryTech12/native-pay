import logging
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services import bmoni_service, groq_service, paystack_service, store, transaction_service, voice_auth, yarngpt_service
from app.services.languages import supported_languages
from app.services.transaction_service import STATES

logger = logging.getLogger("nativepay")

app = FastAPI(title="NativePay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon simplicity — tighten to the real frontend origin before production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"ok": True, "demoMode": True, "bmoniMockMode": bmoni_service.is_mock_mode()}


@app.get("/api/languages")
def languages():
    return supported_languages()


class TtsBody(BaseModel):
    text: str
    language: str = "en"


@app.post("/api/tts")
async def tts(body: TtsBody):
    try:
        audio = await yarngpt_service.synthesize_speech(body.text, body.language)
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as err:
        logger.error("tts failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "TTS_UNAVAILABLE", "message": str(err)})


@app.post("/api/voice/process")
async def voice_process(audio: UploadFile = File(...), language: Optional[str] = Form(None)):
    try:
        audio_bytes = await audio.read()
        text = await groq_service.transcribe_audio(audio_bytes, audio.filename, language)
        intent = await groq_service.parse_intent(text)
        return {"text": text, "intent": intent.model_dump()}
    except Exception as err:
        logger.error("voice_process failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...), language: Optional[str] = Form(None)):
    try:
        audio_bytes = await audio.read()
        text = await groq_service.transcribe_audio(audio_bytes, audio.filename, language)
        return {"text": text}
    except Exception as err:
        logger.error("transcribe failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


class IntentTextBody(BaseModel):
    text: str


@app.post("/api/ai/intent")
async def ai_intent(body: IntentTextBody):
    try:
        return (await groq_service.parse_intent(body.text)).model_dump()
    except Exception as err:
        logger.error("ai_intent failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


class ConfirmBody(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    action: Optional[str] = None
    amount: Optional[int] = None
    recipient: Optional[str] = None
    confidence: Optional[float] = None


@app.post("/api/transactions/confirm")
def transactions_confirm(body: ConfirmBody):
    if not body.id:
        evaluated = transaction_service.evaluate_intent(
            user_id=body.userId or "mama-aisha",
            action=body.action or "unknown",
            amount=body.amount,
            recipient=body.recipient,
            confidence=body.confidence,
        )
        return evaluated

    existing = store.get_transaction(body.id)
    if not existing:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    if existing.state != STATES["CONFIRMATION_REQUIRED"]:
        raise HTTPException(status_code=409, detail={"error": "INVALID_STATE", "state": existing.state})
    return transaction_service.confirm_transaction(body.id)


@app.post("/api/transactions/{tx_id}/cancel")
def transactions_cancel(tx_id: str):
    result = transaction_service.cancel_transaction(tx_id)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return result


class VerifyFaceBody(BaseModel):
    id: str
    matched: bool = False


@app.get("/api/banks")
async def banks():
    try:
        return await paystack_service.list_banks()
    except Exception as err:
        logger.error("banks failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BANKS_UNAVAILABLE", "message": str(err)})


@app.get("/api/paystack/resolve-account")
async def paystack_resolve_account(accountNumber: str, bankCode: str):
    """Standalone test/utility endpoint — resolves an account directly,
    with no transaction required. What resolve-recipient calls internally."""
    try:
        return await paystack_service.resolve_account(accountNumber, bankCode)
    except Exception as err:
        logger.error("paystack_resolve_account failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "ACCOUNT_NOT_FOUND", "message": str(err)})


class ResolveRecipientBody(BaseModel):
    id: str
    accountNumber: str
    bankCode: str


@app.post("/api/transactions/resolve-recipient")
async def transactions_resolve_recipient(body: ResolveRecipientBody):
    result = await transaction_service.resolve_recipient_by_account(body.id, body.accountNumber, body.bankCode)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return result


@app.post("/api/transactions/verify-face")
def transactions_verify_face(body: VerifyFaceBody):
    result = transaction_service.record_face_verification(body.id, body.matched)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return result


class SendBody(BaseModel):
    id: str


@app.post("/api/transactions/send")
async def transactions_send(body: SendBody):
    try:
        result = await transaction_service.execute_transaction(body.id)
        if not result:
            raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
        return result
    except HTTPException:
        raise
    except Exception as err:
        logger.error("transactions_send failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/transactions")
def transactions_list(userId: Optional[str] = None):
    return store.list_transactions(userId)


@app.get("/api/transactions/{tx_id}")
def transactions_get(tx_id: str):
    tx = store.get_transaction(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return tx


@app.get("/api/transactions/{tx_id}/receipt")
def transactions_receipt(tx_id: str):
    tx = store.get_transaction(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    if tx.state != STATES["TRANSACTION_SUCCESS"]:
        raise HTTPException(status_code=409, detail={"error": "RECEIPT_NOT_AVAILABLE", "state": tx.state})
    return bmoni_service.generate_receipt(tx)


@app.post("/api/bmoni/generate-owner-wallet")
def bmoni_generate_owner_wallet():
    """One-time setup helper — generates an EVM keypair for the
    self-custodied smart-wallet owner. Save privateKey as
    BMONI_OWNER_PRIVATE_KEY in .env, then never call this again."""
    return bmoni_service.generate_owner_wallet()


class BmoniCreateUserBody(BaseModel):
    firstName: str
    email: str
    phoneNumber: str


@app.post("/api/bmoni/users")
async def bmoni_create_user(body: BmoniCreateUserBody):
    try:
        return await bmoni_service.create_user(body.firstName, body.email, body.phoneNumber)
    except Exception as err:
        logger.error("bmoni_create_user failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.post("/api/bmoni/users/{user_id}/wallet")
async def bmoni_create_wallet(user_id: str):
    try:
        return await bmoni_service.create_smart_wallet(user_id)
    except Exception as err:
        logger.error("bmoni_create_wallet failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


class BmoniKycBody(BaseModel):
    bvn: str = bmoni_service.SANDBOX_TEST_BVN
    countryCode: str = bmoni_service.SANDBOX_COUNTRY_CODE


@app.post("/api/bmoni/users/{user_id}/kyc")
async def bmoni_submit_kyc(user_id: str, body: BmoniKycBody):
    try:
        return await bmoni_service.submit_kyc(user_id, body.bvn, body.countryCode)
    except Exception as err:
        logger.error("bmoni_submit_kyc failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/bmoni/users/{user_id}/onboarding-status")
async def bmoni_onboarding_status(user_id: str):
    try:
        return await bmoni_service.get_onboarding_status(user_id)
    except Exception as err:
        logger.error("bmoni_onboarding_status failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


class BmoniActivateBody(BaseModel):
    walletAddress: str
    walletIndex: int = 0
    bvn: str = bmoni_service.SANDBOX_TEST_BVN


@app.post("/api/bmoni/users/{user_id}/activate-nigeria")
async def bmoni_activate_nigeria(user_id: str, body: BmoniActivateBody):
    try:
        return await bmoni_service.activate_nigeria_rail(user_id, body.walletAddress, body.walletIndex, body.bvn)
    except Exception as err:
        logger.error("bmoni_activate_nigeria failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/bmoni/users/{user_id}/wallets")
async def bmoni_get_wallets(user_id: str):
    try:
        return await bmoni_service.get_wallets(user_id)
    except Exception as err:
        logger.error("bmoni_get_wallets failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/bmoni/users/{user_id}/real-balances")
async def bmoni_get_real_balances(user_id: str):
    try:
        return await bmoni_service.get_real_balances(user_id)
    except Exception as err:
        logger.error("bmoni_get_real_balances failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/bmoni/users/{user_id}/real-transactions")
async def bmoni_get_real_transactions(user_id: str):
    try:
        return await bmoni_service.get_real_transactions(user_id)
    except Exception as err:
        logger.error("bmoni_get_real_transactions failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BMONI_API_ERROR", "message": str(err)})


@app.get("/api/accounts/{account_id}/balance")
def accounts_balance(account_id: str):
    try:
        balance = transaction_service.get_account_balance(account_id)
        return {"accountId": account_id, "balance": balance, "currency": "NGN"}
    except Exception as err:
        logger.error("accounts_balance failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "BMONI_API_ERROR", "message": str(err)})


class AccountRegisterBody(BaseModel):
    userId: str
    fullName: str
    address: str
    language: str


@app.post("/api/accounts/register")
def accounts_register(body: AccountRegisterBody):
    if store.get_account(body.userId):
        raise HTTPException(status_code=409, detail={"error": "ACCOUNT_EXISTS"})
    account = store.create_account(body.userId, body.fullName, body.language, body.address)
    return account


@app.get("/api/accounts/by-card/{card_number}")
def accounts_get_by_card(card_number: str):
    account = store.get_account_by_card(card_number)
    if not account:
        raise HTTPException(status_code=404, detail={"error": "CARD_NOT_RECOGNIZED"})
    return account


@app.get("/api/accounts/{account_id}")
def accounts_get(account_id: str):
    account = store.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail={"error": "ACCOUNT_NOT_FOUND"})
    return account


class VoiceprintBody(BaseModel):
    userId: str
    featureVector: list[float]


@app.post("/api/voice/register")
def voice_register(body: VoiceprintBody):
    return voice_auth.register_voiceprint(body.userId, body.featureVector)


@app.post("/api/voice/authorize")
def voice_authorize(body: VoiceprintBody):
    return voice_auth.authorize_by_voice(body.userId, body.featureVector)


@app.get("/api/voice/status/{user_id}")
def voice_status(user_id: str):
    return {"registered": voice_auth.has_voiceprint(user_id)}
