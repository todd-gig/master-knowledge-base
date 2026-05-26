# Legacy DRIVE_SCOPES Sunset Plan (intelligence-silo)

**Status:** PROPOSAL — awaiting decision
**Authored:** 2026-05-25
**Author:** Explore subagent (`a7d51a21f7b100a54`), reviewed by Claude main session
**Companion:** [PR #40 — drive→drive.file scope downgrade for WRITE flow](https://github.com/todd-gig/intelligence-silo/pull/40)

---

## 1. The decision needed

We just downgraded `DRIVE_SCOPES_WRITE` from full `drive` (restricted tier) to `drive.file` (non-sensitive) to unblock publishing the OAuth consent screen. That covers the multi-account write flow.

The legacy single-account flow still uses a SECOND scope set, `DRIVE_SCOPES`, defined at `intelligence-silo/core/drive_oauth.py:52-56`:

```python
DRIVE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.readonly",
]
```

`drive.readonly` is in Google's **SENSITIVE** tier. When the consent screen is published:
- Works for users, but shows the "Google hasn't verified this app" interstitial
- Hard cap at ~100 active users
- Must be verified within 12 months of publish

Three options on the table.

---

## 2. What the legacy flow actually does

**Endpoint:** `POST /v1/intelligence/sync/google-drive` (`intelligence-silo/core/api.py:888-965`)

**API calls:**
1. `list_recent_docs(user_id)` — `GET /drive/v3/files` with query `(mimeType='application/vnd.google-apps.document') and trashed=false`. Returns a list of all the user's Google Docs.
2. `export_doc_text(user_id, file_id)` — `GET /drive/v3/files/{id}/export` with `mimeType=text/plain` for each Doc. Chunks by paragraph, ingests into memory.

**UX:** "Connect your Drive → we list all your Docs → we ingest the ones you want." No Picker step; the silo enumerates the user's Drive directly.

**Token storage:** SQLite `oauth_tokens` table — legacy rows have `account_email IS NULL`; multi-account rows have `account_email IS NOT NULL`.

**Why `drive.file` can't substitute:** `drive.file` only grants access to files the app created OR files explicitly opened via Google Picker. The legacy flow's "list everything" UX requires either `drive.readonly` (Sensitive) or full `drive` (Restricted). No Picker step exists in v0.5.

---

## 3. Three options

### Option A — Downgrade legacy to `drive.file` + Picker
- **Effort:** High
  - FE Picker UI component + integration in `/sources` page
  - Picker callback handler in BE to receive selected file IDs
  - Migration of existing rows / forced re-auth path
- **User impact:** UX regression — users must hand-pick files via Picker instead of auto-listing
- **Consent screen:** ✅ Non-sensitive; no warning; no user cap
- **Verification:** None needed

### Option B — Sunset legacy flow, force migration to v1 multi-account
- **Effort:** Medium-high
  - Add `/v1/oauth/drive/migrate` endpoint
  - Deprecation window (60 days) with banner in `/sources`
  - Delete legacy rows after cutoff
- **User impact:** One-time re-auth via multi-account flow; lose single-account UX entirely
- **Consent screen:** ✅ Non-sensitive (multi-account already uses `drive.file` post PR #40)
- **Verification:** None needed
- **Bonus:** Simplifies codebase to a single OAuth path

### Option C — Keep `drive.readonly`, accept the constraints
- **Effort:** None
- **User impact:** None now; may hit 100-user cap if popular
- **Consent screen:** ⚠️ Sensitive tier; warning persists; 100-user cap; verification required within 12 months
- **Verification:** Needed within 12mo (Google audit, ~4-8 weeks)

---

## 4. Recommendation matrix

| Aspect | A: drive.file + Picker | B: Sunset legacy | C: Keep readonly |
|---|---|---|---|
| Implementation effort | High | Medium | None |
| User-visible impact | High (UX change) | High (re-auth once) | None now; cap later |
| Consent screen publish | ✅ Non-sensitive | ✅ Non-sensitive | ⚠️ Sensitive, warning |
| Google verification | Not needed | Not needed | Needed within 12mo |
| Code complexity | Higher (dual-path) | Lower (single path) | Lower (no change) |
| User cap | None | None | 100 unverified |

**RECOMMENDATION: Option B (Sunset legacy)**

Why:
- Consent screen warning + cap on Option C is a permanent drag until verification clears (and verification for `drive.readonly` is non-trivial)
- Option A's UX regression (Picker for every file) is worse than a one-time re-auth
- v1 multi-account is already live and is the future; consolidating there is the right direction
- Codebase simplification is a free win

---

## 5. Sunset execution plan

### 5.1 Pre-decision (run BEFORE committing to Option B)

Query the prod SQLite `oauth_tokens` table to count active legacy users:

```sql
SELECT COUNT(DISTINCT user_id)
FROM oauth_tokens
WHERE provider = 'google_drive'
  AND account_email IS NULL
  AND last_refreshed_at > DATE('now', '-30 days');
```

If the count is **< 10**, skip the deprecation window and silently migrate (notify users post-migration).
If **10-100**, run the full deprecation window below.
If **> 100**, reconsider — Option C's verification path might be worth it.

### 5.2 Deprecation window (if needed)

| Day | Action |
|---|---|
| D-0 | Ship `/sources` banner: "The single-account Drive flow is being retired on YYYY-MM-DD. Reconnect via Multi-Account to keep ingestion working." |
| D-0 | Ship `/v1/oauth/drive/migrate` endpoint that initiates the v1 multi-account flow with the legacy user's email pre-populated |
| D-0 | Email all legacy users (extracted via the query above) with the migration link |
| D-30 | Second email; banner becomes red/urgent |
| D-60 | Final email |
| D-60 +1d | Disable `GET /v1/oauth/drive/start` (legacy entry point) |
| D-60 +1d | Delete legacy rows from `oauth_tokens` |
| D-60 +1d | Remove `DRIVE_SCOPES` constant + `list_recent_docs` + `export_doc_text` from `core/drive_oauth.py` |
| D-60 +1d | Remove `POST /v1/intelligence/sync/google-drive` endpoint from `core/api.py` |

### 5.3 Code changes (single PR after deprecation window)

Files to remove/modify in `intelligence-silo`:
- `core/drive_oauth.py` lines 52-56 — delete `DRIVE_SCOPES` constant
- `core/drive_oauth.py` lines ~222-242 — delete `build_authorization_url()` (v0.5)
- `core/drive_oauth.py` lines ~463-530 — delete `store_tokens()` (v0.5 storage)
- `core/drive_oauth.py` lines ~695-784 — delete `get_fresh_access_token()` legacy lookup path
- `core/drive_oauth.py` lines ~784, ~820 — delete `list_recent_docs()` and `export_doc_text()`
- `core/api.py` lines 805-816 — delete `GET /v1/oauth/drive/start` (legacy)
- `core/api.py` lines 888-965 — delete `POST /v1/intelligence/sync/google-drive`
- `core/api.py` line ~847 — simplify callback (no more `__legacy__` label handling)
- Tests: remove any legacy-specific assertions; keep the multi-account suite

### 5.4 OAuth consent screen update

After the sunset:
- Edit consent screen at `console.cloud.google.com/auth/scopes?project=carmen-beach-properties` (or `gigaton-platform` post-migration)
- **Remove** `https://www.googleapis.com/auth/drive.readonly`
- Keep `https://www.googleapis.com/auth/drive.file` + `openid` + `userinfo.email`
- App stays in "In Production" status, no verification needed for the remaining non-sensitive scope set

---

## 6. File references (current state)

- **Scope definitions:** `core/drive_oauth.py:52-69`
- **Legacy OAuth start:** `core/drive_oauth.py:222-242`; `core/api.py:805-816`
- **Legacy token storage:** `core/drive_oauth.py:463-530`; `core/api.py:847` (callback routing)
- **Legacy Drive API use:** `core/api.py:888-965` (POST `/v1/intelligence/sync/google-drive`)
- **Database schema:** `core/drive_oauth.py:338-444` (SQLite DDL); `migrations/030_documentation_ingest.sql`
- **PR #40 commit:** `03e08bc` — downgraded `DRIVE_SCOPES_WRITE` to `drive.file` on 2026-05-25
