"""Engagement stress persistence mixin.

Stores the derived user-side stress score for a conversation. The score is
computed by engines/engagement_stress.py from the existing engagement pieces
(will message signals, pressure state, message text) and written only when it
changes (band transition or delta above floor), keeping the table a readable
trajectory instead of per-message noise.

Schema is created idempotently via `CREATE TABLE IF NOT EXISTS` and is never
destructive - aligned with the AGENTS.md schema compatibility rule.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

STRESS_BANDS = ("low", "medium", "high")


def _band_for(score: float) -> str:
    if score >= 0.66:
        return "high"
    if score >= 0.33:
        return "medium"
    return "low"


class EngagementStressDatabaseMixin:
    """Database mixin for persisting and querying engagement stress scores."""

    def _init_engagement_stress_schema(self) -> None:
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_engagement_stress_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    persona TEXT,
                    conversation_id INTEGER,
                    cycle_id TEXT,
                    stress_score REAL NOT NULL,
                    stress_band TEXT,
                    input_signal_id INTEGER,
                    components_json TEXT,
                    prev_score REAL,
                    score_delta REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_engagement_stress_user_created "
                "ON agent_engagement_stress_scores(user_id, created_at DESC)"
            )
            self.conn.commit()

    def save_engagement_stress_score(
        self,
        *,
        user_id: str,
        stress_score: float,
        persona: Optional[str] = None,
        conversation_id: Optional[int] = None,
        cycle_id: Optional[str] = None,
        input_signal_id: Optional[int] = None,
        components: Optional[Dict[str, Any]] = None,
        min_delta: float = 0.15,
    ) -> Optional[Dict[str, Any]]:
        """Write a stress score row, but only on meaningful change.

        Returns the persisted row dict when a row was written, else None.
        """
        self._init_engagement_stress_schema()
        score = max(0.0, min(1.0, float(stress_score)))
        band = _band_for(score)
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT stress_score, stress_band FROM agent_engagement_stress_scores
                WHERE user_id = ? ORDER BY id DESC LIMIT 1
                """,
                (str(user_id),),
            )
            row = cursor.fetchone()
            if row is not None:
                prev_score = float(row["stress_score"] or 0.0)
                prev_band = str(row["stress_band"] or _band_for(prev_score))
                delta = score - prev_score
                if band == prev_band and abs(delta) < min_delta:
                    return None
                prev_values = (prev_score, delta)
            else:
                prev_values = (None, None)

            cursor.execute(
                """
                INSERT INTO agent_engagement_stress_scores
                    (user_id, persona, conversation_id, cycle_id, stress_score, stress_band,
                     input_signal_id, components_json, prev_score, score_delta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(user_id),
                    persona,
                    conversation_id,
                    cycle_id,
                    score,
                    band,
                    input_signal_id,
                    json.dumps(components or {}, ensure_ascii=False, default=str),
                    prev_values[0],
                    prev_values[1],
                ),
            )
            self.conn.commit()
            return {
                "id": cursor.lastrowid,
                "user_id": str(user_id),
                "persona": persona,
                "stress_score": score,
                "stress_band": band,
                "prev_score": prev_values[0],
                "score_delta": prev_values[1],
            }

    def get_latest_engagement_stress_score(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Latest recorded stress score for a user, parsed with components."""
        self._init_engagement_stress_schema()
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM agent_engagement_stress_scores
                WHERE user_id = ? ORDER BY id DESC LIMIT 1
                """,
                (str(user_id),),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        result = dict(row)
        try:
            result["components"] = json.loads(result.pop("components_json") or "{}")
        except Exception as exc:
            logger.warning("[ENGAGEMENT_STRESS] components_json ilegivel: %s", exc)
            result["components"] = {}
        return result
