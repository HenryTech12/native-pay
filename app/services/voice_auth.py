"""
Lightweight heuristic voiceprint check — MFCC feature vectors (extracted
client-side with Meyda.js) compared via cosine similarity. A real signal,
NOT trained speaker-verification. Facial capture remains the actual
authorization gate; this only decides whether to skip straight to it.

Storage is in-memory for the hackathon demo — swap for a real datastore
before this goes anywhere near production or a second server instance.
"""

import math
import os

_voiceprints: dict[str, list[float]] = {}

THRESHOLD = float(os.environ.get("VOICE_MATCH_THRESHOLD", "0.85"))

# Stricter than the login threshold — this one can skip the mandatory
# face check for a transaction, so it demands a much higher-confidence
# match than "good enough to skip straight to the app" at login.
TRANSACTION_THRESHOLD = float(os.environ.get("TRANSACTION_VOICE_MATCH_THRESHOLD", "0.92"))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def register_voiceprint(user_id: str, feature_vector: list[float]) -> dict:
    _voiceprints[user_id] = feature_vector
    return {"registered": True, "userId": user_id}


def authorize_by_voice(user_id: str, feature_vector: list[float]) -> dict:
    stored = _voiceprints.get(user_id)
    if stored is None:
        return {"authorized": False, "reason": "no_registered_voiceprint"}
    similarity = _cosine_similarity(stored, feature_vector)
    return {"authorized": similarity >= THRESHOLD, "similarity": round(similarity, 3), "threshold": THRESHOLD}


def authorize_for_transaction(user_id: str, feature_vector: list[float]) -> dict:
    """Stricter check used to decide whether a transaction's mandatory
    face check can be skipped — same mechanism as authorize_by_voice,
    higher bar, because this one authorizes money movement rather than
    just a login shortcut."""
    stored = _voiceprints.get(user_id)
    if stored is None:
        return {"authorized": False, "reason": "no_registered_voiceprint"}
    similarity = _cosine_similarity(stored, feature_vector)
    return {"authorized": similarity >= TRANSACTION_THRESHOLD, "similarity": round(similarity, 3), "threshold": TRANSACTION_THRESHOLD}


def has_voiceprint(user_id: str) -> bool:
    return user_id in _voiceprints
