"""Tests for engagement stress scoring and write-on-change persistence."""
import sqlite3
import sys
import types
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

openai_stub = types.ModuleType("openai")
openai_stub.OpenAI = object
if not hasattr(sys.modules.get("openai"), "OpenAI"):
    sys.modules["openai"] = openai_stub

import engines.engagement_stress as es
from core.db.engagement_stress import EngagementStressDatabaseMixin, _band_for


USER_ID = "user-1"


class FakeDB(EngagementStressDatabaseMixin):
    def __init__(self, conn):
        self.conn = conn
        self._lock = __import__("threading").RLock()


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL
        );
        CREATE TABLE agent_will_message_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            saber_delta REAL DEFAULT 0.34,
            relacionar_delta REAL DEFAULT 0.33,
            expressar_delta REAL DEFAULT 0.33,
            dominant_signal TEXT
        );
        CREATE TABLE agent_will_pressure_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            cycle_id TEXT NOT NULL,
            saber_pressure REAL DEFAULT 0,
            relacionar_pressure REAL DEFAULT 0,
            expressar_pressure REAL DEFAULT 0
        );
        """
    )
    conn.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (USER_ID, "Test"))
    conn.commit()
    return FakeDB(conn)


def _add_signal(db, saber=0.34, relacionar=0.33, expressar=0.33):
    db.conn.execute(
        "INSERT INTO agent_will_message_signals (user_id, saber_delta, relacionar_delta, expressar_delta) VALUES (?, ?, ?, ?)",
        (USER_ID, saber, relacionar, expressar),
    )
    db.conn.commit()


# ---------------- scoring ----------------

def test_band_thresholds():
    assert _band_for(0.1) == "low"
    assert _band_for(0.5) == "medium"
    assert _band_for(0.9) == "high"


def test_calm_message_scores_low():
    comps = es.score_message_text("oi, tudo bem? tive um dia normal")
    assert comps["lexicon"] == 0.0
    assert comps["intensity"] < 0.2


def test_distress_message_scores_high_lexicon():
    comps = es.score_message_text("nao aguento mais isso, estou em desespero total")
    assert comps["lexicon"] >= 0.6


def test_intensity_components():
    comps = es.score_message_text("NAO AGUENTO MAIS!!!")
    assert comps["intensity"] > 0.1


# ---------------- persistence ----------------

def test_first_score_is_written():
    db = _make_db()
    row = db.save_engagement_stress_score(user_id=USER_ID, stress_score=0.2, persona="sienna")
    assert row is not None
    assert row["stress_band"] == "low"
    assert row["persona"] == "sienna"
    assert row["prev_score"] is None


def test_no_write_without_change():
    db = _make_db()
    db.save_engagement_stress_score(user_id=USER_ID, stress_score=0.2)
    assert db.save_engagement_stress_score(user_id=USER_ID, stress_score=0.25) is None
    # band change forces a write
    row = db.save_engagement_stress_score(user_id=USER_ID, stress_score=0.5)
    assert row is not None and row["stress_band"] == "medium"
    assert row["prev_score"] == 0.2


def test_get_latest_round_trip():
    db = _make_db()
    db.save_engagement_stress_score(
        user_id=USER_ID, stress_score=0.7, components={"lexicon": 0.6, "intensity": 0.1}
    )
    latest = db.get_latest_engagement_stress_score(USER_ID)
    assert latest["stress_band"] == "high"
    assert latest["components"]["lexicon"] == 0.6


# ---------------- engine ----------------

def test_engine_score_exchange_end_to_end():
    db = _make_db()
    _add_signal(db, saber=0.2, relacionar=0.6, expressar=0.2)
    engine = es.EngagementStressEngine(db)
    row = engine.score_exchange(
        user_id=USER_ID,
        user_input="estou muito ansioso e sobrecarregado com tudo ultimamente",
        persona="sienna",
        conversation_id=1,
    )
    assert row is not None
    assert 0.0 <= row["stress_score"] <= 1.0
    latest = db.get_latest_engagement_stress_score(USER_ID)
    assert latest["persona"] == "sienna"
    assert "lexicon" in latest["components"]
    assert "signal_trend" in latest["components"]


def test_engine_clamps_scores():
    db = _make_db()
    engine = es.EngagementStressEngine(db)
    row = engine.score_exchange(user_id=USER_ID, user_input="DESUPERACULPADO!!!")
    assert row is None or 0.0 <= row["stress_score"] <= 1.0


def test_schema_idempotent():
    db = _make_db()
    db._init_engagement_stress_schema()
    db._init_engagement_stress_schema()
    db.save_engagement_stress_score(user_id=USER_ID, stress_score=0.1)
    assert db.get_latest_engagement_stress_score(USER_ID) is not None
