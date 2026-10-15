# JungAgent — Project Status
## Session of October 14–15, 2026

**Instance:** `jung_v1` / persona "sienna" / single-admin R&D
**Branch:** `vibe/mem0-2x-adapter-92a189`
**State:** server running, all subsystems operational, enhancement queue pending

---

## 1. What We Found (Session Forensics)

### Fresh-install bug class (all fixed)
Three instances of the same pattern — schedulers/code racing lazy table creation:
1. Will-pressure scheduler vs `rumination_tensions` → fixed (boot-order commit)
2. Fact extraction vs `user_facts_v2` → fixed (manual DDL; never created by any boot path)
3. Hobby phase vs `rumination_insights` → covered by the same boot-order fix

### Hidden-failure class
- **Mojibake logger**: corrupted UTF-8 in source strings crashed error logging mid-write, hiding a one-line exception (`no such table: user_facts_v2`) for an entire day. Fixed: ASCII-only error calls.
- **mem0 2.x API drift**: jung's adapter used the pre-2.x `search(user_id=, limit=)` shape; mem0 2.2.1 requires `filters=/top_k=`. Fixed across all call sites.

### Architecture findings
- **The persona canon was being silently rejected** by the C12f cognitive-ownership gate (`persona_core` was not a registered domain). Her in-character replies were path-dependent: active-consciousness path worked (directive appended to prompt), standard path dropped the canon. Fixed: domain registered + contract aligned + injection carries the global origin class. Verified: canon now passes on every message.
- **The clinical frame (`STANDARD_IDENTITY_PROMPT`) never applied to admin** — the admin path uses the frame-free `ADMIN_IDENTITY_PROMPT`. The "Jungian pull" in admin replies came from the `Jung:` completion anchor + semantic context, both now counterweighted by the persona voice directive.
- **Hybrid memory is real and verified**: semantic (mem0→Qdrant, ~10 memories/message) + structured (`user_facts_v2`, 61+ facts, live extraction working, backfilled from history). Recall proven live: she synthesizes facts into insight, not just recites.
- **The digestion cascade works**: conversations → facts → fragments (5 and growing) → [tensions → insights → dreams: expected as material accumulates] → identity. Overnight: hobby phase produced 4 textual artifacts (first real expressive output); will engine re-weighted from saber→expressar dominance across two cycles.
- **Confabulation gap (design finding)**: with a starving dream subsystem, her self-reports of inner life were beautiful fiction (the "cal-mex logo dream" had no `agent_dreams` row behind it). Fixed with the anchoring clause: inner-life reports must draw from actual remembered material; honest emptiness over invented content.

### Security/ops hygiene established
- Keys: shared (OpenRouter, Qdrant, Groq, Venice, HF, telethon) in `~/.zshrc`; jung-specific (bot token, admin IDs, persona/provider config) in jung's `.env`. One key rotation completed (OpenRouter, after transcript exposure). `.envBackup` flagged for gitignore.
- Admin identity derivation: `ADMIN_PLATFORM_ID` → hashed `ADMIN_USER_ID` (`c9980df44eb1994d`), consistent across runtime; the `remote_db_probe.py` user_id display is a known cosmetic bug (reads legacy scope).

---

## 2. Current Changes (shipped on the branch)

| # | Change | Commit |
|---|---|---|
| 1 | mem0 2.x adapter (filters/top_k) | early |
| 2 | Dashboard missing-table guard + logger fix | early |
| 3 | `/start` welcome Markdown fix | early |
| 4 | Rumination tables created at boot | boot-order |
| 5 | Persona layer: canon (identity/voice/psychology/capabilities), deep psychology blocks (governing logic, values, motives, tensions, social model, work model) | series |
| 6 | Persona voice directive at `_call_conversation_llm` choke point (all reply paths) | choke-point commit |
| 7 | `persona_core` registered as C12f domain + contract aligned + INSTANCE_GLOBAL injection | 58958fd/1c2a9d5 |
| 8 | Photo commands: `/photo` + `/photo_nsfw` → sienna content server SFW/NSFW album contracts (structural 404 isolation between tiers) | series |
| 9 | Photo aliases: `/image /pic /pict /picture` (+_nsfw) | 651cea4 |
| 10 | Venice.ai provider (private, uncensored; `LLM_PROVIDER=venice` switch; conversation routing; parked on OpenRouter as daily) | series |
| 11 | Extractor NoneType guard | 651cea4 |
| 12 | ASCII error logger (mojibake fix) | 651cea4 |
| 13 | Persona anchoring clause (no fabricated inner experiences) | 16f0c00 |

**Upstream contribution status:** 13 commits of fresh-install fixes + the persona layer, PR #2 material (draft, https://github.com/themeaux/jungclaude/pull/2). The sienna repo carries the content-server album contracts (PR #3 draft).

---

## 3. Planned Changes (queue, unordered priority)

### Small repairs (next batch)
- **TRI upsert**: `INSERT OR IGNORE` (or accumulation) for duplicate Big Five fragments — repeated detection currently warns and saves nothing; evidence should accumulate confidence for psychometrics.
- **Will-signal column**: `no such column: user_id` in the micro-signal persistence — diagnose (`PRAGMA table_info(agent_will_message_signals)`) and fix via ALTER or code.
- **Stale working-memory cleanup**: the three resolved hobby-failure items still rebroadcast every phase.
- **Admin user row**: healthcheck's "safe repair" (one click on `/admin/instance/setup`).
- **`user_facts_v2` in schema init**: make the boot path create the table (the manual DDL should not be the only creation path) — upstream-worthy.
- **OpenRouter-key config-read order**: the engine's second check warns despite a working key (import-time read vs dotenv load order).
- **`.envBackup` gitignore line.**

### Enhancement: the psychology-models extension (Hillman+)
Multi-school depth psychology as interpretive lenses, in three integration depths:
1. **Phase 1 (canon file)**: `persona/sienna/psychology_models.md` — Hillman (image-first, anti-translation), Freud (defense/repetition), Klein (splitting/objects), Winnicott (holding/good-enough), Kelly (construct grid/triads), McAdams (narrative identity), + loader method in `persona_layer.py`. Changes her interpretive voice; lens selection as clinical judgment.
2. **Phase 2 (cognition)**: Kelly constructs as a `user_constructs` table (bipolar dimensions in the user's own vocabulary — richer than Big Five); triad-question flows feeding psychometrics.
3. **Phase 3 (detection)**: Klein/Freud signatures as TRI fragment types (splitting language, repetition patterns) — new rumination material classes.
4. **Phase 4 (dream integration)**: Hillman stance in dream conversations — stay with the image, cite `dream#id` material, pair with the anchoring clause.
- **Open decision**: primacy — one school as her default center of gravity, or plural per-material selection.

### Architectural (post-repair)
- **Multi-agent runner**: `agents/` directory convention, per-agent `.env` (AGENT_INSTANCE, PERSONA_NAME, provider posture), one process per persona. Jung is already instance-scoped end-to-end (DB, Qdrant collection, loop state) — the runner is orchestration, not architecture. Candidate second persona: Cassie (bible exists in sienna repo).
- **Identity seeding**: canon traits into `agent_identity_core` as foundational beliefs (high initial certainty, evidence=bible) so the emergent self starts shaped and evolves from there. Needs the drift-assessment tool (canon vs crystallized comparison).
- **Multi-user containment** (the audit's finding): the algorithmic temenos — interpretive brakes for non-admin users; DBT-style structure is the leading candidate. Prerequisite for any multi-user product; the system's own introspection independently arrived at this requirement.
- **Provider routing**: traffic-aware cost switch (idle → Groq Dev Tier for scheduled calls; OpenRouter for conversation). World scheduler is hourly (not 5-min) — actual overnight cost measured at $0.37.
- **Always-on deployment**: launchd or Railway; currently the organism lives only while `python main.py` runs.

### Documentation
- This file. The session annotation (`SESSION_ANNOTATION_2026_10_15_VALIDATION.md`) exists but is gitignored by the repo's `docs/` exclusion — decide: exception line or relocate.

---

## 4. Standing decisions (recorded for context)

- **Jungian frame: intact by choice.** The maintainer's clinical design (non-therapist rules, CVV protocol) is preserved and tested. The persona layer coexists with it; the admin path is frame-free by the repo's own design.
- **Provider posture: OpenRouter daily / Venice one-switch / Groq for volume.** The uncensored test was a capability verification, not a posture change.
- **Anchoring over immersion**: inner-life reports are honest (Extension C applied). Multi-user would require Extension A (disclosed seams) — see the containment item.
- **The repo's own conventions rule upstream contributions**: evidence anchors (`tipo#id`), no silent exceptions, tests before merge, cost registration for new LLM calls.
