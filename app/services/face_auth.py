"""
Real facial verification — 128-dimension face descriptors extracted
client-side with face-api.js (a dlib ResNet face-recognition model
running via TensorFlow.js in the browser), compared here via Euclidean
distance. This is the same descriptor-comparison technique used by
face_recognition/dlib-based systems generally, not a toy.

Only the descriptor (128 floats) is ever sent to or stored by this
backend — never a raw photo. Storage is in-memory for the hackathon
demo — swap for a real datastore before this goes anywhere near
production or a second server instance.

0.6 is face-api.js's own documented threshold for "same person" on its
reference model; kept configurable since real-world camera/lighting
conditions can shift what's appropriate.
"""

import math
import os

_face_descriptors: dict[str, list[float]] = {}

THRESHOLD = float(os.environ.get("FACE_MATCH_THRESHOLD", "0.6"))


def _euclidean_distance(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return float("inf")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def register_face(user_id: str, descriptor: list[float]) -> dict:
    _face_descriptors[user_id] = descriptor
    return {"registered": True, "userId": user_id}


def authorize_by_face(user_id: str, descriptor: list[float]) -> dict:
    stored = _face_descriptors.get(user_id)
    if stored is None:
        return {"authorized": False, "reason": "no_registered_face"}
    distance = _euclidean_distance(stored, descriptor)
    return {"authorized": distance <= THRESHOLD, "distance": round(distance, 3), "threshold": THRESHOLD}


def has_face(user_id: str) -> bool:
    return user_id in _face_descriptors
