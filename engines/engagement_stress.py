"""Engagement stress scoring engine.

Listens to the existing engagement pieces (will message signals, pressure
state, message text) and derives a user-side stress score in [0, 1] per
exchange. Scores are persisted by core/db/engagement_stress.py only when they
change (band transition or delta above floor) - this module only computes.

This is a data-collection phase: scores and their components are recorded so
the interpretive-lens module (Hillman/Freud/etc. selection) can be calibrated
against real trajectories later. No LLM calls; purely lexical + signal based.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Distress lexicon (pt-BR + en). Hits contribute to the lexical component.
LEXICON_HIGH = (
    "nao aguento", "não aguento", "desespero", "desesperada", "desesperado",
    "panic", "panico", "pânico", "panicked", "breakdown", "surto",
    "quero sumir", "want to disappear", "can't take it", "cant take it",
    "acabou comigo", "destroyed me", "hate myself", "me odeio", "worthless",
    "inutil", "inútil", "hopeless", "sem saida", "sem saída", "suicid",
)
LEXICON_MEDIUM = (
    "ansiedade", "anxiety", "anxious", "ansioso", "ansiosa", "stressed",
    "estressad", "overwhelmed", "sobrecarregad", "exhausted", "exaust",
    "cansad", "tired of", "deprimid", "depressed", "triste", "sad",
    "sozinh", "lonely", "sozinho", "medo", "afraid", "scared", "worried",
    "preocupad", "nervos", "nervous", "frustrad", "frustrat", "irritad",
    "angry", "raiva", "bravo", "chatead", "upset", "hurt", "machucad",
    "dor", "pain", "culpa", "guilt", "shame", "vergonha",
)
INTENSIFIERS = (
    "muito", "so much", "too much", "demais", "extremely", "extremamente",
    "really", "really", "sempre", "always", "never", "nunca", "todo dia",
    "every day", "constant", "constante",
)

_CAPS_RUN = re.compile(r"\b[A-Z]{4,}\b")
_EXCLAM_RUN = re.compile(r"!{2,}")
_QSTN_RUN = re.compile(r"\?{2,}")


def _count_hits(text: str, terms: tuple) -> int:
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def score_message_text(user_input: str) -> Dict[str, float]:
    """Lexical + intensity read of a single user message. Returns components in [0, 1]."""
    text = user_input or ""
    if not text.strip():
        return {"lexicon": 0.0, "intensity": 0.0}

    lexicon = 0.0
    high = _count_hits(text, LEXICON_HIGH)
    med = _count_hits(text, LEXICON_MEDIUM)
    if high:
        lexicon = min(1.0, 0.6 + 0.2 * high)
    elif med:
        lexicon = min(0.55, 0.2 + 0.12 * med)

    intensity = 0.0
    caps = len(_CAPS_RUN.findall(text))
    exclam = len(_EXCLAM_RUN.findall(text))
    qstn = len(_QSTN_RUN.findall(text))
    intensifiers = _count_hits(text, INTENSIFIERS)
    if len(text) > 0:
        caps_ratio = caps / max(1.0, len(text.split()))
        intensity = min(1.0, 0.3 * caps_ratio * 4 + 0.15 * exclam + 0.1 * qstn + 0.05 * intensifiers)

    return {"lexicon": round(lexicon, 3), "intensity": round(intensity, 3)}


def score_recent_signals(recent_signals: List[Dict[str, Any]]) -> Dict[str, float]:
    """Trend read of the last will message signals (deltas + summaries)."""
    if not recent_signals:
        return {"signal_trend": 0.0}
    n = len(recent_signals)
    expressar = [float(s.get("expressar_delta") or 0.0) for s in recent_signals]
    relacionar = [float(s.get("relacionar_delta") or 0.0) for s in recent_signals]
    saber = [float(s.get("saber_delta") or 0.0) for s in recent_signals]
    # swings: erratic expressar deltas + suppressed relacionar read as distress
    swing = max(expressar) - min(expressar) if n else 0.0
    avg_rel = sum(relacionar) / n
    avg_sab = sum(saber) / n
    signal_trend = min(1.0, 0.5 * swing + 0.25 * max(0.0, 0.34 - avg_rel) * 2 + 0.25 * max(0.0, avg_sab - 0.5))
    return {"signal_trend": round(min(1.0, signal_trend), 3)}


class EngagementStressEngine:
    """Computes and persists the user engagement stress score."""

    WEIGHTS = {"lexicon": 0.45, "intensity": 0.20, "signal_trend": 0.20, "pressure": 0.15}
    RECENT_SIGNAL_WINDOW = 5

    def __init__(self, db_manager: Any):
        self.db = db_manager

    def _recent_signals(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                """
                SELECT saber_delta, relacionar_delta, expressar_delta, dominant_signal
                FROM agent_will_message_signals
                WHERE user_id = ? ORDER BY id DESC LIMIT ?
                """,
                (str(user_id), self.RECENT_SIGNAL_WINDOW),
            )
            return [dict(r) for r in cursor.fetchall()]
        except Exception as exc:
            logger.warning("[ENGAGEMENT_STRESS] falha ao ler sinais recentes: %s", exc)
            return []

    def _pressure_component(self, user_id: str) -> float:
        try:
            from will_pressure import load_latest_pressure_state
            state = load_latest_pressure_state(self.db, user_id)
            if not state:
                return 0.0
            avg = (
                float(state.get("saber_pressure") or 0.0)
                + float(state.get("relacionar_pressure") or 0.0)
                + float(state.get("expressar_pressure") or 0.0)
            ) / 3.0
            return min(1.0, avg)
        except Exception as exc:
            logger.warning("[ENGAGEMENT_STRESS] falha ao ler estado de pressao: %s", exc)
            return 0.0

    def score_exchange(
        self,
        *,
        user_id: str,
        user_input: str,
        input_signal_id: Optional[int] = None,
        conversation_id: Optional[int] = None,
        cycle_id: Optional[str] = None,
        persona: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Score one exchange and persist if changed. Returns the row or None."""
        text_components = score_message_text(user_input)
        signal_components = score_recent_signals(self._recent_signals(user_id))
        pressure = self._pressure_component(user_id)

        components = {
            **text_components,
            **signal_components,
            "pressure": round(pressure, 3),
            "message_chars": len(user_input or ""),
        }
        score = sum(
            weight * components.get(key, 0.0)
            for key, weight in self.WEIGHTS.items()
        )
        score = max(0.0, min(1.0, score))

        return self.db.save_engagement_stress_score(
            user_id=user_id,
            stress_score=score,
            persona=persona,
            conversation_id=conversation_id,
            cycle_id=cycle_id,
            input_signal_id=input_signal_id,
            components=components,
        )
