# Proposal: AX-024 — Cloud Run Secret References Must Point to ENABLED Versions

**Status:** PROPOSAL — pending triad sign-off (Todd / Matt / Bella) per master plan §6
**Severity:** MAJ
**Proposed by:** Phase C-G sprint debrief, 2026-05-21
**Revised:** 2026-05-22 (review-driven fixes to statement scope, project resolution, CI auth, regex coverage, perf)
**Cost of not adopting:** ~3 hours of deploy cascade debugging per incident (validated empirically 2026-05-21 00:03–03:30Z — 3 consecutive deploy failures rooted in this exact class of error)
**Effort to implement handler:** ~120 lines of Python (handler + helpers); reuses existing drift_sentinel structural-handler infrastructure (mirrors AX-021/022/023 pattern)

---

## Axiom statement

> Every `--set-secrets=<ENV_VAR>=<secret_name>:<version>` (or `--update-secrets=…`) reference in any `cloudbuild*.yaml` must, at deploy time, resolve to a secret version that exists in Secret Manager and is in state `ENABLED`. For `:latest` references the secret must have at least one ENABLED version; for a pinned version `:<N>` the named version itself must be ENABLED. Cloud Run rejects any revision whose secret references resolve to a missing or non-ENABLED version, blocking the deploy.

The earlier proposal phrasing ("at least one ENABLED version") was too weak: a pinned `:3` reference passes that check whenever any version is enabled, even if version 3 is disabled — yet Cloud Run still rejects. The handler below checks the requested version specifically.

---

## Scope

- `cloudbuild*.yaml` files at any path under the included repos (NOT Dockerfiles — `--set-secrets` is a `gcloud run deploy` flag, never appears in Dockerfiles).
- Repos: gigaton-gateway, user-access-engine, human-management-engine, persona-engine, ppeme, intelligence-silo, decision-engine, sales-operating-system, connector-api, sovereign-influence-engine, gignet-orchestrator-fn, gignet-activity-emitter-fn (i.e., every repo currently in `local_codebase.include_repos` that ships a `cloudbuild.yaml`).

## Detection logic (revised — 5 fixes applied)

```python
# Module-level cache: prevents N gcloud calls per (project, secret) when
# the same secret is referenced from multiple cloudbuild files in one scan.
_AX024_VERSION_STATE_CACHE: dict[tuple[str, str], list[tuple[str, str]] | None] = {}

# Captures both --set-secrets= and --update-secrets= flags.
_AX024_SECRETS_FLAG_RE = re.compile(r'--(?:set|update)-secrets[=\s]+(\S+)')
_AX024_PROJECT_FLAG_RE = re.compile(r'--project[=\s]+([\w\$\{\}-]+)')


def _ax024_collapse_continuations(text: str) -> str:
    # Collapse `\<newline>` bash line-continuations so multi-line arg
    # lists parse as a single logical line.
    return re.sub(r'\\\s*\n\s*', ' ', text)


def _ax024_resolve_project(text: str) -> str:
    # 1. --project=<X> flag in the cloudbuild args (preferred).
    # 2. $PROJECT_ID / ${PROJECT_ID} -> env PROJECT_ID or DRIFT_GCP_PROJECT.
    # 3. Static default 'gigaton-platform' (matches current deploy reality).
    m = _AX024_PROJECT_FLAG_RE.search(text)
    if m:
        proj = m.group(1)
        if '$PROJECT_ID' in proj or '${PROJECT_ID}' in proj:
            return (os.environ.get('PROJECT_ID')
                    or os.environ.get('DRIFT_GCP_PROJECT')
                    or 'gigaton-platform')
        return proj
    return os.environ.get('DRIFT_GCP_PROJECT', 'gigaton-platform')


def _ax024_query_versions(project, secret, *, timeout=15):
    # Returns (rows, skip_reason). rows is list[(version_name, state)] on
    # success, None on skip. Memoized per (project, secret) for the scan run.
    key = (project, secret)
    if key in _AX024_VERSION_STATE_CACHE:
        cached = _AX024_VERSION_STATE_CACHE[key]
        return (None, 'cached_skip') if cached is None else (cached, None)
    try:
        result = subprocess.run(
            ['gcloud', 'secrets', 'versions', 'list', secret,
             '--project', project, '--format', 'value(name,state)',
             '--limit', '50'],
            capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError:
        _AX024_VERSION_STATE_CACHE[key] = None
        return None, 'gcloud_not_installed'
    except subprocess.TimeoutExpired:
        _AX024_VERSION_STATE_CACHE[key] = None
        return None, 'gcloud_timeout'
    if result.returncode != 0:
        _AX024_VERSION_STATE_CACHE[key] = None
        return None, f'gcloud_error: {result.stderr.strip()[:200]}'
    rows: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            rows.append((parts[0], parts[1]))
    _AX024_VERSION_STATE_CACHE[key] = rows
    return rows, None


def _check_ax_024_empty_secret_version(art, rule):
    if art.metadata.get('ext') not in {'.yaml', '.yml'}:
        return []
    if not Path(art.identifier).name.lower().startswith('cloudbuild'):
        return []
    if 'noqa: AX-024' in art.content:
        return []

    collapsed = _ax024_collapse_continuations(art.content)
    project = _ax024_resolve_project(collapsed)

    # Test override: artifact metadata may stub the version-state oracle.
    # Mirrors the AX-021 pattern of accepting `metadata['git_log']` so the
    # handler is unit-testable without live gcloud auth.
    stub = art.metadata.get('_ax024_version_states')

    violations = []
    for m in _AX024_SECRETS_FLAG_RE.finditer(collapsed):
        blob = m.group(1).strip('"\'')
        for pair in blob.split(','):
            pair = pair.strip()
            if '=' not in pair:
                continue
            env_var, ref = pair.split('=', 1)
            if ':' not in ref:
                continue
            secret_name, version = ref.rsplit(':', 1)

            if stub is not None:
                rows = stub.get((project, secret_name))
                skip_reason = None if rows is not None else 'stub_no_data'
            else:
                rows, skip_reason = _ax024_query_versions(project, secret_name)

            if rows is None:
                violations.append(Violation(
                    rule_id=rule['id'], severity='info',
                    artifact=art.identifier, location=art.identifier,
                    excerpt=(f'AX-024 skipped for {secret_name} in project '
                             f'{project}: {skip_reason}'),
                    suggested_fix='Authenticate gcloud (WIF in CI) to enable enforcement.',
                ))
                continue

            if version == 'latest':
                if not any(state == 'ENABLED' for _, state in rows):
                    violations.append(_ax024_violation(
                        art, rule, secret_name, version, project,
                        reason='no enabled versions'))
            else:
                requested_ok = any(
                    state == 'ENABLED' and (vn == version
                                            or vn.endswith(f'/versions/{version}'))
                    for vn, state in rows)
                if not requested_ok:
                    violations.append(_ax024_violation(
                        art, rule, secret_name, version, project,
                        reason=f'pinned version {version} not ENABLED'))
    return violations
```

### What changed vs the original proposal

1. **Statement tightened** — pinned version `:<N>` must be ENABLED, not "any version ENABLED".
2. **Project resolution made concrete** — three-tier fallback: `--project=` flag → `$PROJECT_ID` env / `DRIFT_GCP_PROJECT` → static default. Original called this "infer from cloudbuild substitutions or default" without specifying.
3. **CI auth gap addressed** — see new "CI wiring" section below.
4. **Regex + scope corrected** — adds `--update-secrets`; drops Dockerfile (irrelevant); handles line-continuation via `_ax024_collapse_continuations`.
5. **Per-scan memoization** — module-level `_AX024_VERSION_STATE_CACHE` keyed on `(project, secret)` so N references to the same secret cost 1 gcloud call.

Also: `Violation` shape now matches the existing AX-021/022/023 handlers (`artifact`, `location`, `excerpt`, `suggested_fix`) — not the `(rule_id, message, remediation, artifact_path)` shape in the original draft.

## Tests

`tests/test_drift_ax_024.py` (mirrors `test_drift_ax_021.py` structure — uses `metadata['_ax024_version_states']` stub to avoid live gcloud calls):

**Original 7:**

- secret with 1 ENABLED `:latest` reference → no violation
- secret with 0 versions referenced as `:latest` → MAJ violation
- specific version `:1` ENABLED → no violation
- gcloud unavailable (stub returns None) → info-severity skip, not crash
- cloudbuild.yaml with no `--set-secrets` → no-op
- multi-secret blob `A=a:latest,B=b:latest,C=c:latest` → each independently checked
- non-cloudbuild yaml not scanned

**Added 4 (this revision):**

- pinned `:3` requested but only `:1` ENABLED → MAJ violation (Fix #1)
- secret with all versions DISABLED → MAJ violation
- `--update-secrets=` flag variant detected (Fix #4)
- multi-line bash `args:` with `\` continuation parses correctly (Fix #4)
- `$PROJECT_ID` substitution resolves via env override (Fix #2)
- `# noqa: AX-024` suppresses
- memoization: 3 references to same secret → 1 stub lookup (Fix #5)

## Why MAJ (not CRIT, not MIN)

- **Not CRIT** — doesn't leak credentials, doesn't break tenant isolation, doesn't compromise integrity. It just blocks deploys (annoying but recoverable).
- **Not MIN** — costs real engineering time per incident. Empirical: 2026-05-21 cascade = 3 failed deploys, 3.5 hours of debug + recovery, partial revert of PR #37, master plan doctrine drift correction needed. MIN severity would let this slip into a digest weeks later.
- **MAJ** matches the operational cost: surfaces in weekly drift report + can block CI pre-merge if wired to `--fail-on major`.

## Where AX-024 would have caught the 2026-05-21 cascade

The trigger: PR #37 added `OPENAI_API_KEY=openai-api-key:latest` to gigaton-gateway/cloudbuild.yaml at 2026-05-20T23:53Z. The slot `openai-api-key` was created earlier but never had a version added.

If AX-024 had been wired into the drift sentinel scan in CI (with gcloud auth):
- PR #37 CI run would have surfaced: `MAJ: AX-024 violation: cloudbuild references openai-api-key:latest (project=gigaton-platform) but no enabled versions. Cloud Run will reject the revision.`
- Either the PR would have been blocked OR the reviewer would have caught it
- Saved 3.5 hours of cascade debug + the partial revert

## How to apply

### Step 1 — Add axiom to `decision-engine/drift_sentinel/axioms.yaml`

```yaml
- axiom_id: AX-024
  statement: "Cloud Run --set-secrets / --update-secrets references in cloudbuild*.yaml must resolve to a Secret Manager version that exists and is ENABLED at deploy time (':latest' requires any enabled version; ':<N>' requires that specific version enabled)."
  scope: ["all_repos"]
  detection_rule: "structural_handler:_check_ax_024_empty_secret_version"
  severity: MAJ
  established: 2026-05-22
  supersedes: null
```

### Step 2 — Append handler + helpers to `drift_sentinel/drift_scan.py`

~120 lines per spec above.

### Step 3 — Register in `STRUCTURAL_HANDLERS` dict

```python
"AX-024": _check_ax_024_empty_secret_version,
```

### Step 4 — Add to `AXIOM_REGISTRY.md`

Bump header `23 axioms` → `24 axioms`; add full AX-024 section.

### Step 5 — Add to `DRIFT_RULES.yaml`

Add the rule in the Phase F block; add `AX-024` to `source_routing.local_codebase.rules_applied`.

### Step 6 — Add tests at `tests/test_drift_ax_024.py`

11 tests — see above.

### Step 7 — Open PR

`feat(drift_sentinel): AX-024 — empty/disabled secret version detection` against decision-engine.

### Step 8 — CI wiring (CRITICAL — without this, AX-024 never fires in CI)

The drift_scan handler degrades to `severity=info` whenever gcloud is unauthenticated. In GHA without Workload Identity Federation wired into the drift_scan job, *every* AX-024 check will silently skip — so the prevention story collapses. Two options:

**Option A (recommended)** — drift_scan GHA job authenticates to each target GCP project via WIF before running:

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ vars.WIF_PROVIDER }}
    service_account: drift-sentinel@gigaton-platform.iam.gserviceaccount.com
- run: python -m drift_sentinel.drift_scan --source local_codebase --fail-on major
```

The SA needs `roles/secretmanager.viewer` on every project that hosts secrets referenced in any scanned `cloudbuild.yaml` (currently: `gigaton-platform`, `carmen-beach-properties`, `ti-solutions`).

**Option B** — run AX-024 as a separate post-deploy GHA step *inside each deploy workflow*, reusing the deploy's existing gcloud auth (already scoped to the right project). Simpler IAM, but means the check fires at deploy time, not PR time.

## Cross-references

- Root-cause incident report: [empty_secret_slot_deploy_failure.md](empty_secret_slot_deploy_failure.md)
- Master plan §3.3.1 — PR #37 partial revert + OpenAI route status
- decision-engine PR #62 (Phase F drift rules) — handler + tests pattern to mirror
- decision-engine `drift_sentinel/AXIOM_REGISTRY.md` — current 23 axioms (24 after this lands)
- Review notes 2026-05-22 (5 fixes incorporated into this revision)
