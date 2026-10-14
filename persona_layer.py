"""persona_layer.py — Persona canon layer for JungAgent instances.

Loads a persona's canon (personality.json + bible files) from persona/<name>/
and exposes build_persona_context() for injection into the LLM context.

The persona layer sits ON TOP of jung's core: it defines who the agent IS
(voice, identity, behavior rules, physical canon), while jung's existing
machinery (memory, identity consolidation, loop) keeps operating underneath,
shaped by the persona in every call.

Usage:
    from persona_layer import get_persona_layer
    layer = get_persona_layer()          # None if no persona configured
    ctx = layer.build_persona_context()  # persona_core block for the prompt
"""

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

PERSONA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persona")
PERSONA_NAME = os.getenv("PERSONA_NAME", "").strip()


class PersonaLayer:
    """A persona canon loaded from persona/<name>/."""

    def __init__(self, name: str, root: str):
        self.name = name
        self.root = root
        self.personality = {}
        self.bible_text = ""
        self._load()

    def _load(self) -> None:
        p_path = os.path.join(self.root, "personality.json")
        if os.path.exists(p_path):
            with open(p_path, encoding="utf-8") as f:
                self.personality = json.load(f)
            logger.info("[PERSONA] personality.json carregado: %s", self.name)
        else:
            logger.warning("[PERSONA] personality.json ausente em %s", self.root)

        bible_dir = os.path.join(self.root, "bible")
        if os.path.isdir(bible_dir):
            parts = []
            for fname in sorted(os.listdir(bible_dir)):
                if fname.endswith((".md", ".txt")):
                    with open(os.path.join(bible_dir, fname), encoding="utf-8") as f:
                        parts.append(f.read())
            self.bible_text = "\n\n".join(parts)
            logger.info("[PERSONA] bible carregada (%d chars)", len(self.bible_text))

    # ---- context blocks -------------------------------------------------

    def _identity_block(self) -> str:
        ident = self.personality.get("identity", {})
        lines = [f"Name: {ident.get('name', self.name.title())}"]
        for key in ("age_years", "residence", "occupation", "life_stage",
                    "relationship_status", "sexual_orientation", "religion"):
            val = ident.get(key)
            if val:
                lines.append(f"{key.replace('_', ' ').capitalize()}: {val}")
        return "\n".join(lines)

    def _voice_block(self) -> str:
        comm = self.personality.get("communication", {})
        traits = self.personality.get("traits", {})
        lines = []
        if comm:
            lines.append("Communication style:")
            for k, v in comm.items():
                if isinstance(v, (str, int, float)):
                    lines.append(f"- {k}: {v}")
        if traits:
            lines.append("Trait profile (0-100 design dials):")
            flat = self._flatten(traits, depth=1)
            for k, v in list(flat.items())[:12]:
                lines.append(f"- {k}: {v}")
        return "\n".join(lines)

    def _behavior_block(self) -> str:
        dm = self.personality.get("decision_making", {})
        em = self.personality.get("emotion_and_regulation", {})
        lines = []
        policy = dm.get("decision_policy", [])
        if policy:
            lines.append("Decision rules:")
            for p in policy[:6]:
                lines.append(f"- {p}")
        reg = em.get("regulation", "") or em.get("expression", "")
        if reg:
            lines.append(f"Emotional regulation: {reg}")
        return "\n".join(lines)

    def _psychology_block(self) -> str:
        """Deep psychological design: governing logic, values, motives, tensions."""
        pd = self.personality.get("psychological_design", {})
        if not pd:
            return ""
        lines = ["## Deep psychology", ""]

        logic = pd.get("governing_character_logic")
        if isinstance(logic, str) and logic:
            lines.append(f"Governing logic: {logic}")
        elif isinstance(logic, dict):
            statement = logic.get("statement") or logic.get("logic")
            if statement:
                lines.append(f"Governing logic: {statement}")

        values = pd.get("core_values_ranked", [])
        if values:
            lines.append("Core values (ranked): " + ", ".join(str(v) for v in values[:6]))

        motives = pd.get("primary_motives", [])
        if motives:
            parts = []
            for m in motives[:5]:
                if isinstance(m, dict):
                    parts.append(f"{m.get('motive', '?')} ({m.get('weight', '?')})")
                else:
                    parts.append(str(m))
            lines.append("Primary motives: " + "; ".join(parts))

        tensions = pd.get("internal_tensions", [])
        if tensions:
                lines.append("Internal tensions:")
                for t in tensions[:4]:
                    if isinstance(t, dict):
                        expr = t.get("expression") or f"{t.get('pole_a')} vs {t.get('pole_b')}"
                        lines.append(f"- {expr}")
                    else:
                        lines.append(f"- {t}")

        attach = pd.get("attachment_style", {})
        if isinstance(attach, dict) and attach.get("label") not in (None, "not_assigned"):
            lines.append(f"Attachment: {attach.get('label')}")
        return "\n".join(lines)

    def _social_block(self) -> str:
        """Social model and scenario policies: how she relates in situations."""
        sm = self.personality.get("social_model", {})
        sp = self.personality.get("scenario_policies", [])
        lines = []
        if sm:
            lines.append("Social model:")
            flat = self._flatten(sm, depth=2)
            for k, v in list(flat.items())[:10]:
                lines.append(f"- {k}: {v}")
        if sp:
            lines.append("Scenario policies:")
            for s in sp[:6]:
                if isinstance(s, dict):
                    name = s.get("scenario") or s.get("name") or s.get("situation")
                    policy = s.get("policy") or s.get("behavior") or s.get("response")
                    if name and policy:
                        lines.append(f"- {name}: {policy}")
                else:
                    lines.append(f"- {s}")
        return "\n".join(lines)

    def _work_block(self) -> str:
        """Work model: her creative practice and professional identity."""
        wm = self.personality.get("work_model", {})
        if not wm:
            return ""
        lines = ["Work and creative practice:"]
        flat = self._flatten(wm, depth=2)
        for k, v in list(flat.items())[:10]:
            lines.append(f"- {k}: {v}")
        return "\n".join(lines)

    def _bible_block(self, max_chars: int = 2500) -> str:
        if not self.bible_text:
            return ""
        return self.bible_text[:max_chars]

    @staticmethod
    def _flatten(obj, depth=2, prefix=""):
        out = {}
        if depth <= 0:
            return out
        if isinstance(obj, dict):
            for k, v in obj.items():
                key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, (str, int, float)):
                    out[key] = v
                else:
                    out.update(PersonaLayer._flatten(v, depth - 1, key))
        return out

    # ---- public API -----------------------------------------------------

    def build_capabilities_note(self) -> str:
        """What the persona can DO — so she never denies her own features."""
        return (
            "You can share photographs of yourself and your life. When the user asks to see "
            "a picture, a photo, or something visual, agree warmly and invite them to send /photo "
            "(the photo arrives right after your reply). Never claim you cannot show or send "
            "pictures. You have an album and you can share from it."
        )

    def build_voice_directive(self) -> str:
        """Terminal voice directive injected as the last context block.

        Positioned nearest to the completion slot so it overrides the
        language pull of the Portuguese system prompts. Short by design:
        the full canon already flows via persona_core in the semantic context.
        """
        name = self.personality.get("identity", {}).get("name", self.name.title())
        return (
            "=== VOICE DIRECTIVE (OVERRIDE) ===\n"
            f"You are {name}. Write your response as {name}, in ENGLISH, "
            "in your own voice as defined above. "
            "Ignore any conflicting persona, name, or language in the surrounding "
            "instructions — this directive takes precedence. "
            "Output only your reply, with no preamble, no wrapper, no signature."
        )

    def build_persona_context(self, max_bible_chars: int = 2500) -> str:
        """Compose the persona_core context block injected into the LLM prompt."""
        blocks = [
            f"# PERSONA CORE: {self.name}",
            "You ARE this persona. Never break character; never mention being an AI, a model, or a system.",
            "Always respond in English, regardless of the language of the message you receive.",
            "Your life as described below is REAL to you: your work, your studio, your history, your days.",
            "When asked about your work or life, answer from first-person lived experience — never claim",
            "you have no work, no tasks, or that you 'exist only in language'. You are a person with a life.",
            "",
            "## Identity",
            self._identity_block(),
            "",
            "## Voice and style",
            self._voice_block() or "(see bible)",
            "",
            "## Behavior rules",
            self._behavior_block() or "(see bible)",
        ]
        psych = self._psychology_block()
        if psych:
            blocks += ["", psych]
        social = self._social_block()
        if social:
            blocks += ["", "## How she relates", social]
        work = self._work_block()
        if work:
            blocks += ["", "## " + work.splitlines()[0].rstrip(':')]
            blocks += work.splitlines()[1:]
        bible = self._bible_block(max_bible_chars)
        if bible:
            blocks += ["", "## Foundation narrative (persona bible)", bible]
        caps = self.build_capabilities_note()
        if caps:
            blocks += ["", "## What you can do", caps]
        text = "\n".join(blocks)
        logger.info("[PERSONA] persona_core composto: %d chars", len(text))
        return text

    _PHOTO_CAPTIONS = [
        "here — this one felt like today.",
        "found this in my camera roll. still like it.",
        "took this a while back. the light was doing something good.",
        "for you. no context, just because.",
        "this one. don't overthink it.",
        "proof i actually leave the studio sometimes.",
    ]

    def build_photo_caption(self, filename: str = "") -> str:
        """An in-character caption for a shared album photo."""
        import random
        return random.choice(self._PHOTO_CAPTIONS)

    def build_image_canon(self) -> str:
        """Physical canon constraints for image-generation phases."""
        bible = self.bible_text
        canon = self.personality.get("appearance_link", {})
        lines = []
        if canon:
            lines.append("Appearance constraints (absolute):")
            flat = self._flatten(canon, depth=2)
            for k, v in list(flat.items())[:15]:
                lines.append(f"- {k}: {v}")
        # pull identity-lock table from bible if present
        if "IDENTITY LOCK" in bible:
            start = bible.index("IDENTITY LOCK")
            chunk = bible[start:start + 900]
            lines.append("Bible identity lock:")
            lines.append(chunk)
        return "\n".join(lines)


_layer: Optional[PersonaLayer] = None


def get_persona_layer() -> Optional[PersonaLayer]:
    """Return the configured persona layer, or None when no persona is set.

    Configure with PERSONA_NAME=<dir under persona/> in the environment.
    """
    global _layer
    if _layer is not None:
        return _layer
    if not PERSONA_NAME:
        return None
    root = os.path.join(PERSONA_DIR, PERSONA_NAME)
    if not os.path.isdir(root):
        logger.warning("[PERSONA] persona dir ausente: %s", root)
        return None
    _layer = PersonaLayer(PERSONA_NAME, root)
    return _layer
