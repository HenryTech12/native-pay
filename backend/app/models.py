from typing import Literal, Optional
from pydantic import BaseModel

Action = Literal["send", "balance", "withdraw", "deposit", "airtime", "bill", "unknown"]

TransactionState = Literal[
    "INTENT_DETECTED",
    "COLLECTING_DETAILS",
    "CONFIRMATION_REQUIRED",
    "USER_CONFIRMED",
    "FACE_VERIFICATION_REQUIRED",
    "FACE_VERIFIED",
    "TRANSACTION_PROCESSING",
    "TRANSACTION_SUCCESS",
    "USER_CANCELLED",
    "INVALID_AMOUNT",
    "INSUFFICIENT_FUNDS",
    "UNKNOWN_RECIPIENT",
    "LOW_AI_CONFIDENCE",
    "TRANSACTION_FAILED",
    "FACE_VERIFICATION_FAILED",
    "BMONI_API_ERROR",
]


class ParsedIntent(BaseModel):
    action: Action = "unknown"
    amount: Optional[int] = None
    recipient: Optional[str] = None
    confidence: float = 0.0


class TransactionRecord(BaseModel):
    id: str
    userId: str
    action: Action
    amount: Optional[int] = None
    recipient: Optional[str] = None
    confidence: Optional[float] = None
    state: TransactionState
    createdAt: str
    faceVerified: bool = False
    bmoniReference: Optional[str] = None
    error: Optional[str] = None
    needsClarification: Optional[Literal["amount", "recipient"]] = None


class Account(BaseModel):
    id: str
    name: str
    preferredLanguage: str
    balance: int
    address: Optional[str] = None
    cardNumber: Optional[str] = None


class Recipient(BaseModel):
    name: str
    account: str


class Receipt(BaseModel):
    transactionId: str
    type: Action
    amount: Optional[int] = None
    recipient: Optional[str] = None
    reference: Optional[str] = None
    status: TransactionState
    date: str
    environment: str
