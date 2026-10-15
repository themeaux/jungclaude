"""API routes for programmatic conversation access.

Each conversation thread is keyed by an API key that IS the conversation id
(= the C12g relation id). Clients obtain a key from the admin (who mints
relations), then POST messages to /api/v1/chat/{key}.

The persona (Sienna), agent identity, dreams and loop state are shared at
the instance level; facts and conversation history are relation-scoped.

Env:
    JUNG_API_KEYS        comma-separated keys (conversation ids) that are
                         accepted by this endpoint. If unset, the endpoint
                         is disabled (fail-closed).
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["api"])


class ChatRequest(BaseModel):
    message: str
    user_name: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_key: str
    response: str
    message_id: Optional[int] = None


def _api_keys() -> set:
    raw = os.getenv("JUNG_API_KEYS", "")
    return {k.strip() for k in raw.split(",") if k.strip()}


def _get_bot_state():
    from telegram_bot import bot_state
    return bot_state


def _ensure_relation_for_key(db, key: str, user_name: Optional[str]) -> str:
    """Ensure a participant user + eligible relation exist for this API key.

    The API key doubles as the relation_id. Relations are created
    active+granted (admin minted the key, which is the consent decision).
    """
    from instance_config import AGENT_INSTANCE

    participant_id = f"api_{key[:8]}"
    try:
        db.create_user(participant_id, user_name or f"api_{key[:8]}",
                       platform="api", platform_id=key)
    except Exception:
        pass  # user may already exist

    relation = db.get_agent_relation(key)
    if relation is None:
        cursor = db.conn.cursor()
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO agent_relations "
            "(relation_id, agent_instance, org_id, participant_user_id, relation_type, role, "
            "status, consent_status, consented_at, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, 'companion', 'primary', 'active', 'granted', ?, ?, ?)",
            (key, AGENT_INSTANCE, "default-org", participant_id, now, now, now),
        )
        db.conn.commit()
        logger.info("[API] relation created for key=%s", key[:8])
    return participant_id


@router.post("/chat/{key}", response_model=ChatResponse)
async def api_chat(key: str, body: ChatRequest, request: Request):
    keys = _api_keys()
    if not keys:
        raise HTTPException(status_code=404, detail="api_disabled")
    if key not in keys:
        raise HTTPException(status_code=401, detail="invalid_key")

    bot_state = _get_bot_state()
    if not bot_state or not bot_state.jung_engine:
        raise HTTPException(status_code=503, detail="engine_unavailable")

    db = bot_state.db
    participant_id = _ensure_relation_for_key(db, key, body.user_name)

    try:
        import asyncio
        result = await asyncio.to_thread(
            bot_state.jung_engine.process_message,
            user_id=participant_id,
            message=body.message,
            chat_history=None,
        )
    except ValueError as exc:
        # relation/consent gate failures
        raise HTTPException(status_code=403, detail=str(exc))
    except Exception as exc:
        logger.error("[API] chat failed key=%s: %s", key[:8], exc)
        raise HTTPException(status_code=500, detail="internal_error")

    response_text = str(result.get("display_response") or result.get("clean_response") or "")
    conversation_id = result.get("conversation_id") if isinstance(result, dict) else None
    return ChatResponse(
        conversation_key=key,
        response=response_text,
        message_id=conversation_id,
    )


@router.get("/status/{key}")
async def api_status(key: str):
    keys = _api_keys()
    if not keys or key not in keys:
        raise HTTPException(status_code=404, detail="not_found")
    bot_state = _get_bot_state()
    if not bot_state:
        raise HTTPException(status_code=503, detail="engine_unavailable")
    db = bot_state.db
    relation = db.get_agent_relation(key)
    if relation is None:
        return {"conversation_key": key, "status": "no_relation"}
    return {
        "conversation_key": key,
        "status": relation.get("status"),
        "consent": relation.get("consent_status"),
        "participant": relation.get("participant_user_id"),
    }
