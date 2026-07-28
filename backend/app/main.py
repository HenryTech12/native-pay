from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services import bmoni_service, groq_service, store, transaction_service, voice_auth
from app.services.languages import supported_languages
from app.services.transaction_service import STATES

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


@app.post("/api/voice/process")
async def voice_process(audio: UploadFile = File(...), language: Optional[str] = Form(None)):
    try:
        audio_bytes = await audio.read()
        text = await groq_service.transcribe_audio(audio_bytes, audio.filename, language)
        intent = await groq_service.parse_intent(text)
        return {"text": text, "intent": intent.model_dump()}
    except Exception as err:
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...), language: Optional[str] = Form(None)):
    try:
        audio_bytes = await audio.read()
        text = await groq_service.transcribe_audio(audio_bytes, audio.filename, language)
        return {"text": text}
    except Exception as err:
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


class IntentTextBody(BaseModel):
    text: str


@app.post("/api/ai/intent")
async def ai_intent(body: IntentTextBody):
    try:
        return (await groq_service.parse_intent(body.text)).model_dump()
    except Exception as err:
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


@app.get("/api/accounts/{account_id}/balance")
def accounts_balance(account_id: str):
    try:
        balance = transaction_service.get_account_balance(account_id)
        return {"accountId": account_id, "balance": balance, "currency": "NGN"}
    except Exception as err:
        raise HTTPException(status_code=500, detail={"error": "BMONI_API_ERROR", "message": str(err)})


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
