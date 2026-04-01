# Converting Files to JSON

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 2/9/2026 21:34:15  
**Updated:** 2/10/2026 17:36:11  
**Exported:** 3/19/2026 16:31:56  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/698a98c0-4e44-8327-85d1-f7d698408f85](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/698a98c0-4e44-8327-85d1-f7d698408f85)  

## Prompt:
Assume Json files will be used to train automated intelligence integrated into the memory system utilizing GME: what types of files can be converted to json and what are the best rules to follow to ensure as much information as possible is encoded into the file

## Response:
What can be converted to JSON
-----------------------------

### 1) Text-first (highest ROI, lowest friction)

*   **Plain text**: `.txt`, `.md`, `.rtf`
*   **Structured docs**: `.docx` (paragraphs, headings, tables), `.html`
*   **Knowledge bases / wikis**: exported HTML/Markdown
*   **Email**: `.eml`, `.msg` (headers + body + thread metadata)

**Conversion pattern**: map to a `Document` object with hierarchical blocks (sections → paragraphs → sentences) plus provenance metadata.

* * *

### 2) Semi-structured business data (easy to normalize)

*   **Spreadsheets**: `.xlsx`, `.csv`, `.tsv`
*   **Databases**: SQL dumps, query results, ORM exports
*   **Forms / surveys**: Typeform, Google Forms exports
*   **CRM exports**: Salesforce/HubSpot exports

**Conversion pattern**: preserve _tables as tables_ (rows/columns + types), and also generate _semantic summaries_ per row/record.

* * *

### 3) Machine-readable artifacts (high leverage for agents)

*   **APIs**: OpenAPI/Swagger, Postman collections
*   **Logs / events**: JSONL, syslog, app logs, audit logs
*   **Configs**: YAML/TOML/INI → JSON
*   **Code + ASTs**: source code → parsed AST + symbol tables (very valuable for causal/dep graphs)
*   **Notion/Confluence exports**: (usually HTML/MD + assets)

**Conversion pattern**: keep the raw artifact + a normalized “analysis layer” (entities, dependencies, call graphs, event schemas).

* * *

### 4) PDFs, images, audio/video (possible, but treat carefully)

*   **PDFs**: text layer extraction; if scanned, OCR is required
*   **Images**: charts, screenshots, diagrams → OCR + layout extraction + (optionally) vision captions
*   **Audio/video**: transcripts + speaker diarization + timestamps; optionally “topic segments”

**Conversion pattern**: store (a) raw media reference, (b) extracted text, (c) structure (pages/regions/timestamps), (d) confidence scores.

* * *

Best rules to encode “maximum information” for GME + memory (without poisoning the system)
------------------------------------------------------------------------------------------

### A) Always use a **3-layer record**: Raw → Canonical → Derived

1.  **Raw**: exact source payload (or a pointer + checksum).
2.  **Canonical**: normalized JSON schema you control (stable over time).
3.  **Derived**: enrichments (entities, relationships, summaries, embeddings refs, classifications).

This prevents the classic failure mode: losing provenance and mixing inference with fact.

* * *

### B) Treat JSON as an **evented knowledge graph**, not a blob

Encode as:

*   **Entities** (people, orgs, systems, concepts, docs)
*   **Relations** (owns, influences, depends\_on, contradicts, supports)
*   **Events** (what happened, when, who, outcome)
*   **Claims** (assertions with evidence + confidence)
*   **Artifacts** (where it came from)

This aligns directly with causal reasoning: _what changed what, when, and why._

* * *

### C) Mandatory provenance fields (non-negotiable)

Every record/block should include:

*   `source.uri` or `source.file_path`
*   `source.type` (pdf, docx, email, transcript, spreadsheet)
*   `source.created_at`, `source.modified_at` (if known)
*   `extraction.method` (native text, OCR, transcript model, manual)
*   `extraction.timestamp`
*   `hash` (sha256 of raw or segment)
*   `segment.address` (page/paragraph/cell/timestamp range)

If you can’t point back to origin, you can’t defend truth in the memory system.

* * *

### D) Preserve structure, not just text

Examples:

*   Docs: headings → sections; lists; tables; footnotes
*   Spreadsheets: workbook → sheet → table regions → cells (with row/col)
*   Transcripts: speaker turns, timestamps, interruptions, overlaps
*   Emails: thread id, reply-to chain, quoted blocks

**Rule**: never flatten a structured document into one string unless you _also_ store the structure.

* * *

### E) Separate **facts vs interpretations**

Use explicit containers:

*   `observations`: extracted/verbatim facts
*   `claims`: statements asserted by a speaker/author
*   `inferences`: model-generated conclusions
*   `recommendations`: proposed actions
*   `assumptions`: unstated requirements

And track:

*   `attribution` (who said it)
*   `confidence` (0–1)
*   `evidence_refs` (segment pointers)

This prevents training a system to “remember hallucinations.”

* * *

### F) Normalize time, identity, and units (where ROI is highest)

*   Times: ISO-8601 + timezone, plus original string
*   People/orgs: stable IDs + alias lists + contact handles
*   Money/units: normalized numeric + original + currency/unit

GME-style causal layers benefit massively from consistent identity and time.

* * *

### G) Use JSONL for scale and retrainability

For pipelines and incremental updates:

*   Prefer **JSON Lines** (`.jsonl`) where each line is one atomic record (event/entity/block).
*   Keep `record_id` stable; use `version` and `supersedes` for updates.

This enables append-only ingestion, replay, and rollback—critical for memory integrity.

* * *

### H) Encode contradictions and deltas explicitly

Add:

*   `contradicts: [record_id...]`
*   `supports: [record_id...]`
*   `supersedes: record_id`
*   `delta`: what changed (before/after)

Causal engines become far more useful when change is first-class.

* * *

### I) Keep schemas strict, but allow extensions

*   Define a **core schema** (required fields)
*   Allow `extensions.{namespace}` for project-specific additions
*   Validate with JSON Schema in CI (yes, even for “data”)

This prevents drift and “schema entropy” over time.

* * *

Practical “best default” JSON object model (minimal but high power)
-------------------------------------------------------------------

Use these top-level record types:

*   `Artifact` (file/email/transcript/spreadsheet)
*   `Block` (a segment: paragraph/cell/speaker turn)
*   `Entity` (person/org/system/concept)
*   `Event` (time-bounded change)
*   `Relation` (typed edge between entities/events/blocks)
*   `Claim` (assertion with evidence)
*   `Task/Decision` (commitments, owners, deadlines)

If you do nothing else: **Artifact + Block + Entity + Claim + Relation** gets you most of the value.

* * *

Anti-patterns that destroy downstream training quality
------------------------------------------------------

*   No provenance (can’t trace anything back)
*   Mixing model summaries into “ground truth” fields
*   Flattening everything into one text field
*   Losing timestamps/speakers/threading
*   Over-normalizing (removing “weird” formatting that carries meaning)
*   Not versioning records (no audit trail)

* * *

Bottom line rules (executive version)
-------------------------------------

1.  **Provenance-first**: every atom traceable to source + location.
2.  **Structure preserved**: hierarchy/tables/timestamps remain intact.
3.  **Facts ≠ inferences**: never co-mingle.
4.  **Event + relation centric**: optimize for causal reasoning, not storage.
5.  **Versioned + appendable**: JSONL, stable IDs, diffs, rollback.

If you want, I can output a concrete JSON Schema for the core objects (Artifact/Block/Entity/Claim/Relation/Event) optimized for GME ingestion and causal indexing.

## Prompt:
create the front end code to be deployed using google studio that guides a user through the process of identifying all pieces of information required to ensure every file uploaded has as much information as possible to ensure accurate education of the automated intelligence, applying the rules of 7s in psychology and the framework previously discussed engineered to ask > answer the WHAT + where + when +why < how questions with the end purpose of the deployed web app to be to auto encode that information into files uploaded > converted on the backend > provided Json file to be manually uploaded

## Response:
Thought for 7s

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>GME JSON Encoder Intake Wizard</title>

    <!-- Tailwind (CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- React 18 (UMD) -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>

    <style>
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
      .focus-ring:focus { outline: none; box-shadow: 0 0 0 3px rgba(59,130,246,0.35); border-color: rgba(59,130,246,1); }
    </style>
  </head>
  <body class="bg-slate-950 text-slate-100">
    <div id="root"></div>

    <script>
      const { useEffect, useMemo, useRef, useState } = React;

      /***********************
       * Utilities
       ***********************/
      function uid(prefix="id") {
        return `${prefix}_${Math.random().toString(16).slice(2)}_${Date.now().toString(16)}`;
      }

      function safeJsonStringify(obj) {
        try { return JSON.stringify(obj, null, 2); } catch (e) { return `/* JSON stringify error: ${String(e)} */`; }
      }

      function downloadText(filename, text, mime="application/json") {
        const blob = new Blob([text], { type: mime });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 500);
      }

      function clamp(n, min, max) { return Math.max(min, Math.min(max, n)); }

      // “Rule of 7s” UX constraint: cap list items to 7 by default.
      const MAX_7 = 7;

      // Local storage persistence
      const LS_KEY = "gme_json_encoder_intake_v1";

      /***********************
       * Schema helpers (front-end manifest format)
       ***********************/
      function newProject() {
        return {
          schema_version: "1.0.0",
          created_at: new Date().toISOString(),
          project: {
            project_id: uid("proj"),
            title: "",
            objective: "",
            owner: "",
            organization: "",
            environment: "prod", // prod|staging|dev
            tags: []
          },
          intake_rules: {
            psychology_rule_of_7s: true,
            max_items_per_list: MAX_7,
            separate_fact_vs_inference: true,
            provenance_first: true,
            preserve_structure: true
          },
          global_context: {
            what: "",
            why: "",
            how: "",
            where: { location: "", system: "", channel: "" },
            when: { start_iso: "", end_iso: "", timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "" }
          },
          entities: [],      // {entity_id, type, name, aliases[], attributes{}, confidence}
          relations: [],     // {relation_id, type, from_ref, to_ref, evidence_refs[], confidence}
          artifacts: [],     // files + metadata
          review: {
            readiness_score: 0,
            missing: [],
            notes: ""
          }
        };
      }

      function newArtifactFromFile(file) {
        return {
          artifact_id: uid("art"),
          file: {
            name: file.name,
            size_bytes: file.size,
            mime_type: file.type || "application/octet-stream",
            last_modified_ms: file.lastModified || null
          },
          source: {
            uri: "",                 // user can paste drive path/url
            origin_system: "",        // e.g. Gmail, Drive, Slack, Zoom, Confluence
            author: "",
            created_at_iso: "",
            modified_at_iso: "",
            confidentiality: "internal", // public|internal|confidential|restricted
            license: ""
          },
          segmentation_hint: {
            type: "auto", // auto|pages|sections|cells|timestamps
            notes: ""
          },
          context_5w1h: {
            what: "",
            where: { location: "", system: "", channel: "" },
            when: { start_iso: "", end_iso: "", timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "" },
            why: "",
            how: ""
          },
          fact_inference_split: {
            observations: [],
            claims: [],
            inferences: [],
            assumptions: []
          },
          gme_causal_layer: {
            events: [],      // {event_id, title, start_iso, end_iso, actors[], inputs[], outputs[], outcome, confidence}
            decisions: [],   // {decision_id, statement, owner, date_iso, rationale, evidence_refs[], confidence}
            tasks: []        // {task_id, title, owner, due_iso, status, dependencies[]}
          },
          quality: {
            extraction_method: "native_text", // native_text|ocr|transcript|manual|mixed
            confidence: 0.8,
            known_gaps: [],
            contradictions: [] // {with_ref, description}
          },
          evidence: {
            citations: [], // {citation_id, quote_under_25_words, pointer, notes}
            attachments: [] // optional future use
          }
        };
      }

      /***********************
       * UI Components
       ***********************/
      function Badge({ children }) {
        return (
          React.createElement("span", { className: "inline-flex items-center rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-200 border border-slate-700" }, children)
        );
      }

      function Section({ title, subtitle, children, right }) {
        return React.createElement(
          "div",
          { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-5 shadow-sm" },
          React.createElement("div", { className: "flex items-start justify-between gap-3" },
            React.createElement("div", null,
              React.createElement("h2", { className: "text-lg font-semibold tracking-tight" }, title),
              subtitle ? React.createElement("p", { className: "mt-1 text-sm text-slate-300" }, subtitle) : null
            ),
            right ? React.createElement("div", null, right) : null
          ),
          React.createElement("div", { className: "mt-4" }, children)
        );
      }

      function TextInput({ label, value, onChange, placeholder, hint }) {
        return React.createElement("div", { className: "space-y-1" },
          React.createElement("label", { className: "text-sm text-slate-200" }, label),
          React.createElement("input", {
            className: "w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus-ring",
            value: value || "",
            placeholder: placeholder || "",
            onChange: (e) => onChange(e.target.value)
          }),
          hint ? React.createElement("div", { className: "text-xs text-slate-400" }, hint) : null
        );
      }

      function TextArea({ label, value, onChange, placeholder, hint, rows=3 }) {
        return React.createElement("div", { className: "space-y-1" },
          React.createElement("label", { className: "text-sm text-slate-200" }, label),
          React.createElement("textarea", {
            className: "w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus-ring",
            value: value || "",
            placeholder: placeholder || "",
            rows,
            onChange: (e) => onChange(e.target.value)
          }),
          hint ? React.createElement("div", { className: "text-xs text-slate-400" }, hint) : null
        );
      }

      function Select({ label, value, onChange, options, hint }) {
        return React.createElement("div", { className: "space-y-1" },
          React.createElement("label", { className: "text-sm text-slate-200" }, label),
          React.createElement("select", {
            className: "w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus-ring",
            value: value || "",
            onChange: (e) => onChange(e.target.value)
          }, options.map(opt => React.createElement("option", { key: opt.value, value: opt.value }, opt.label))),
          hint ? React.createElement("div", { className: "text-xs text-slate-400" }, hint) : null
        );
      }

      function PillButton({ children, onClick, variant="primary", disabled=false }) {
        const base = "rounded-xl px-4 py-2 text-sm font-medium border transition focus-ring";
        const styles = {
          primary: "bg-blue-600 border-blue-500 hover:bg-blue-500 text-white disabled:opacity-50 disabled:hover:bg-blue-600",
          secondary: "bg-slate-900 border-slate-700 hover:bg-slate-800 text-slate-100 disabled:opacity-50",
          danger: "bg-rose-600 border-rose-500 hover:bg-rose-500 text-white disabled:opacity-50 disabled:hover:bg-rose-600"
        };
        return React.createElement("button", { className: `${base} ${styles[variant]}`, onClick, disabled }, children);
      }

      function Progress({ step, total }) {
        const pct = Math.round((step / total) * 100);
        return React.createElement("div", { className: "space-y-2" },
          React.createElement("div", { className: "flex items-center justify-between text-xs text-slate-400" },
            React.createElement("span", null, `Step ${step} / ${total}`),
            React.createElement("span", null, `${pct}%`)
          ),
          React.createElement("div", { className: "h-2 w-full rounded-full bg-slate-900 border border-slate-800 overflow-hidden" },
            React.createElement("div", { className: "h-full bg-blue-600", style: { width: `${pct}%` } })
          )
        );
      }

      function LimitedListEditor({
        title,
        subtitle,
        items,
        onChange,
        placeholder = "Add item...",
        maxItems = MAX_7,
        fields = null, // if provided, items are objects
        objectTemplate = null
      }) {
        const canAdd = items.length < maxItems;

        function addItem() {
          if (!canAdd) return;
          const next = fields ? { ...(objectTemplate || {}), _id: uid("itm") } : "";
          onChange([...items, next]);
        }

        function updateItem(idx, value) {
          const next = [...items];
          next[idx] = value;
          onChange(next);
        }

        function removeItem(idx) {
          const next = items.filter((_, i) => i !== idx);
          onChange(next);
        }

        return React.createElement("div", { className: "rounded-xl border border-slate-800 bg-slate-950/40 p-4" },
          React.createElement("div", { className: "flex items-start justify-between gap-3" },
            React.createElement("div", null,
              React.createElement("div", { className: "flex items-center gap-2" },
                React.createElement("h3", { className: "text-sm font-semibold" }, title),
                React.createElement(Badge, null, `${items.length}/${maxItems}`)
              ),
              subtitle ? React.createElement("p", { className: "mt-1 text-xs text-slate-400" }, subtitle) : null
            ),
            React.createElement(PillButton, { variant: "secondary", onClick: addItem, disabled: !canAdd }, "Add")
          ),

          React.createElement("div", { className: "mt-3 space-y-2" },
            items.length === 0
              ? React.createElement("div", { className: "text-xs text-slate-500" }, "No items yet.")
              : items.map((it, idx) => {
                  if (!fields) {
                    return React.createElement("div", { key: idx, className: "flex gap-2" },
                      React.createElement("input", {
                        className: "flex-1 rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm focus-ring",
                        value: it || "",
                        placeholder,
                        onChange: (e) => updateItem(idx, e.target.value)
                      }),
                      React.createElement(PillButton, { variant: "danger", onClick: () => removeItem(idx) }, "Remove")
                    );
                  }

                  // Object item editor
                  return React.createElement("div", { key: it._id || idx, className: "rounded-xl border border-slate-800 bg-slate-950 p-3" },
                    React.createElement("div", { className: "flex items-center justify-between" },
                      React.createElement("div", { className: "text-xs text-slate-400 mono" }, it._id || ""),
                      React.createElement(PillButton, { variant: "danger", onClick: () => removeItem(idx) }, "Remove")
                    ),
                    React.createElement("div", { className: "mt-2 grid grid-cols-1 md:grid-cols-2 gap-3" },
                      fields.map(f => React.createElement("div", { key: f.key, className: "space-y-1" },
                        React.createElement("label", { className: "text-xs text-slate-300" }, f.label),
                        f.type === "textarea"
                          ? React.createElement("textarea", {
                              className: "w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm focus-ring",
                              rows: 2,
                              value: it[f.key] || "",
                              placeholder: f.placeholder || "",
                              onChange: (e) => updateItem(idx, { ...it, [f.key]: e.target.value })
                            })
                          : React.createElement("input", {
                              className: "w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-sm focus-ring",
                              value: it[f.key] || "",
                              placeholder: f.placeholder || "",
                              onChange: (e) => updateItem(idx, { ...it, [f.key]: e.target.value })
                            })
                      ))
                    )
                  );
                })
          )
        );
      }

      /***********************
       * Scoring / Readiness (simple, explainable)
       ***********************/
      function computeReadiness(project) {
        const missing = [];

        // Project meta
        if (!project.project.title.trim()) missing.push("Project title");
        if (!project.project.objective.trim()) missing.push("Project objective");

        // At least 1 artifact
        if (!project.artifacts.length) missing.push("At least one uploaded file");

        // Global 5W1H (minimum viable)
        const gc = project.global_context;
        if (!gc.what.trim()) missing.push("Global WHAT");
        if (!gc.why.trim()) missing.push("Global WHY");
        if (!gc.where.system.trim()) missing.push("Global WHERE (system)");
        if (!gc.when.timezone.trim()) missing.push("Timezone");

        // Artifact-level minimums
        project.artifacts.forEach((a, i) => {
          const prefix = `File #${i+1} (${a.file.name})`;
          if (!a.source.origin_system.trim()) missing.push(`${prefix}: origin system`);
          if (!a.context_5w1h.what.trim()) missing.push(`${prefix}: WHAT`);
          if (!a.context_5w1h.why.trim()) missing.push(`${prefix}: WHY`);
          if (!a.context_5w1h.where.system.trim()) missing.push(`${prefix}: WHERE (system)`);
          if (!a.quality.extraction_method.trim()) missing.push(`${prefix}: extraction method`);
          // Fact/inference split: at least 1 observation or claim to avoid empty context
          const fis = a.fact_inference_split;
          if ((fis.observations?.length || 0) + (fis.claims?.length || 0) < 1) missing.push(`${prefix}: at least 1 observation or claim`);
        });

        // Score: start 100, subtract per missing item (capped)
        const score = clamp(100 - missing.length * 5, 0, 100);
        return { score, missing };
      }

      /***********************
       * Main App
       ***********************/
      function App() {
        const totalSteps = 5;
        const [step, setStep] = useState(1);
        const [project, setProject] = useState(() => {
          const saved = localStorage.getItem(LS_KEY);
          if (saved) {
            try { return JSON.parse(saved); } catch {}
          }
          return newProject();
        });

        const [selectedArtifactId, setSelectedArtifactId] = useState(null);

        useEffect(() => {
          localStorage.setItem(LS_KEY, safeJsonStringify(project));
        }, [project]);

        const readiness = useMemo(() => computeReadiness(project), [project]);

        useEffect(() => {
          // keep review updated
          setProject(prev => ({
            ...prev,
            review: {
              ...prev.review,
              readiness_score: readiness.score,
              missing: readiness.missing
            }
          }));
          // eslint-disable-next-line react-hooks/exhaustive-deps
        }, [readiness.score, readiness.missing.length]);

        const currentArtifact = useMemo(() => {
          if (!selectedArtifactId) return project.artifacts[0] || null;
          return project.artifacts.find(a => a.artifact_id === selectedArtifactId) || null;
        }, [project.artifacts, selectedArtifactId]);

        function next() { setStep(s => clamp(s + 1, 1, totalSteps)); }
        function prev() { setStep(s => clamp(s - 1, 1, totalSteps)); }

        function resetAll() {
          localStorage.removeItem(LS_KEY);
          setProject(newProject());
          setSelectedArtifactId(null);
          setStep(1);
        }

        function addFiles(fileList) {
          const files = Array.from(fileList || []);
          if (!files.length) return;
          setProject(prev => {
            const nextArtifacts = [...prev.artifacts];
            files.forEach(f => nextArtifacts.push(newArtifactFromFile(f)));
            const next = { ...prev, artifacts: nextArtifacts };
            return next;
          });
        }

        function updateProject(path, value) {
          // minimal path setter
          setProject(prev => {
            const next = structuredClone(prev);
            const keys = path.split(".");
            let cur = next;
            for (let i = 0; i < keys.length - 1; i++) cur = cur[keys[i]];
            cur[keys[keys.length - 1]] = value;
            return next;
          });
        }

        function updateArtifact(artifactId, updater) {
          setProject(prev => {
            const next = structuredClone(prev);
            const idx = next.artifacts.findIndex(a => a.artifact_id === artifactId);
            if (idx === -1) return prev;
            next.artifacts[idx] = updater(next.artifacts[idx]);
            return next;
          });
        }

        function removeArtifact(artifactId) {
          setProject(prev => {
            const next = structuredClone(prev);
            next.artifacts = next.artifacts.filter(a => a.artifact_id !== artifactId);
            return next;
          });
          if (selectedArtifactId === artifactId) setSelectedArtifactId(null);
        }

        function exportManifest() {
          const filename = `gme_intake_manifest_${project.project.project_id}.json`;
          downloadText(filename, safeJsonStringify(project));
        }

        function exportJsonlStubs() {
          // Produce JSONL “atomic records” stubs (artifacts + claims + events) for backend ingestion.
          const lines = [];

          project.artifacts.forEach(a => {
            lines.push(JSON.stringify({
              record_type: "Artifact",
              record_id: a.artifact_id,
              created_at: project.created_at,
              file: a.file,
              source: a.source,
              context_5w1h: a.context_5w1h,
              quality: a.quality
            }));

            (a.fact_inference_split.observations || []).forEach((text, idx) => {
              lines.push(JSON.stringify({
                record_type: "Observation",
                record_id: `${a.artifact_id}:obs:${idx}`,
                artifact_ref: a.artifact_id,
                text,
                attribution: a.source.author || "",
                evidence_ref: { artifact_id: a.artifact_id, pointer: "user_provided" },
                confidence: a.quality.confidence ?? 0.8
              }));
            });

            (a.fact_inference_split.claims || []).forEach((text, idx) => {
              lines.push(JSON.stringify({
                record_type: "Claim",
                record_id: `${a.artifact_id}:clm:${idx}`,
                artifact_ref: a.artifact_id,
                text,
                attribution: a.source.author || "",
                evidence_ref: { artifact_id: a.artifact_id, pointer: "user_provided" },
                confidence: a.quality.confidence ?? 0.8
              }));
            });

            (a.gme_causal_layer.events || []).forEach(ev => {
              const { _id, ...rest } = ev;
              lines.push(JSON.stringify({
                record_type: "Event",
                record_id: ev.event_id || _id || uid("evt"),
                artifact_ref: a.artifact_id,
                ...rest
              }));
            });

            (a.gme_causal_layer.decisions || []).forEach(dc => {
              const { _id, ...rest } = dc;
              lines.push(JSON.stringify({
                record_type: "Decision",
                record_id: dc.decision_id || _id || uid("dec"),
                artifact_ref: a.artifact_id,
                ...rest
              }));
            });

            (a.gme_causal_layer.tasks || []).forEach(tsk => {
              const { _id, ...rest } = tsk;
              lines.push(JSON.stringify({
                record_type: "Task",
                record_id: tsk.task_id || _id || uid("tsk"),
                artifact_ref: a.artifact_id,
                ...rest
              }));
            });
          });

          const filename = `gme_records_${project.project.project_id}.jsonl`;
          downloadText(filename, lines.join("\n"), "application/jsonl");
        }

        const topBar = React.createElement("div", { className: "sticky top-0 z-30 backdrop-blur border-b border-slate-900 bg-slate-950/70" },
          React.createElement("div", { className: "mx-auto max-w-6xl px-4 py-4" },
            React.createElement("div", { className: "flex flex-col gap-3 md:flex-row md:items-center md:justify-between" },
              React.createElement("div", { className: "space-y-1" },
                React.createElement("div", { className: "flex items-center gap-2" },
                  React.createElement("h1", { className: "text-xl font-semibold tracking-tight" }, "GME Intake Wizard"),
                  React.createElement(Badge, null, "Provenance-first"),
                  React.createElement(Badge, null, "5W1H"),
                  React.createElement(Badge, null, "Rule-of-7s")
                ),
                React.createElement("p", { className: "text-sm text-slate-300" },
                  "Guides users to capture maximum metadata so backend conversion can produce high-fidelity JSON for memory + GME causal layers."
                )
              ),
              React.createElement("div", { className: "flex items-center gap-2" },
                React.createElement(PillButton, { variant: "secondary", onClick: exportManifest }, "Export Manifest (.json)"),
                React.createElement(PillButton, { variant: "secondary", onClick: exportJsonlStubs }, "Export Records (.jsonl)"),
                React.createElement(PillButton, { variant: "danger", onClick: resetAll }, "Reset")
              )
            ),
            React.createElement("div", { className: "mt-4 grid grid-cols-1 md:grid-cols-3 gap-4" },
              React.createElement("div", { className: "md:col-span-2" },
                React.createElement(Progress, { step, total: totalSteps })
              ),
              React.createElement("div", { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-4" },
                React.createElement("div", { className: "flex items-center justify-between" },
                  React.createElement("div", { className: "text-sm font-semibold" }, "Readiness"),
                  React.createElement(Badge, null, `${readiness.score}/100`)
                ),
                React.createElement("div", { className: "mt-2 h-2 w-full rounded-full bg-slate-900 border border-slate-800 overflow-hidden" },
                  React.createElement("div", { className: "h-full bg-blue-600", style: { width: `${readiness.score}%` } })
                ),
                React.createElement("div", { className: "mt-2 text-xs text-slate-400" },
                  readiness.missing.length ? `${readiness.missing.length} gap(s) remaining` : "No blocking gaps detected."
                )
              )
            )
          )
        );

        /***********************
         * Step Screens
         ***********************/
        function Step1_ProjectAndFiles() {
          return React.createElement("div", { className: "space-y-6" },
            React.createElement(Section, {
              title: "1) Project setup (global context)",
              subtitle: "These fields become defaults for every uploaded file. Keep them crisp and specific."
            },
              React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4" },
                React.createElement(TextInput, {
                  label: "Project title",
                  value: project.project.title,
                  onChange: v => updateProject("project.title", v),
                  placeholder: "e.g., LiquiFex – Claims Automation Knowledge Pack"
                }),
                React.createElement(TextInput, {
                  label: "Owner",
                  value: project.project.owner,
                  onChange: v => updateProject("project.owner", v),
                  placeholder: "e.g., CxGuy"
                }),
                React.createElement(TextInput, {
                  label: "Organization",
                  value: project.project.organization,
                  onChange: v => updateProject("project.organization", v),
                  placeholder: "e.g., Gigaton / LiquiFex"
                }),
                React.createElement(Select, {
                  label: "Environment",
                  value: project.project.environment,
                  onChange: v => updateProject("project.environment", v),
                  options: [
                    { value: "prod", label: "prod" },
                    { value: "staging", label: "staging" },
                    { value: "dev", label: "dev" }
                  ],
                  hint: "Used by backend pipelines to route processing safely."
                }),
                React.createElement("div", { className: "md:col-span-2" },
                  React.createElement(TextArea, {
                    label: "Objective (WHY this dataset exists)",
                    value: project.project.objective,
                    onChange: v => updateProject("project.objective", v),
                    placeholder: "Define the business outcome and how the automated intelligence will use this information.",
                    rows: 4
                  })
                )
              ),

              React.createElement("div", { className: "mt-6 grid grid-cols-1 md:grid-cols-2 gap-4" },
                React.createElement(TextArea, {
                  label: "Global WHAT (scope)",
                  value: project.global_context.what,
                  onChange: v => updateProject("global_context.what", v),
                  placeholder: "What is the content about? What domain/process/system does it cover?",
                  rows: 3
                }),
                React.createElement(TextArea, {
                  label: "Global WHY (intent)",
                  value: project.global_context.why,
                  onChange: v => updateProject("global_context.why", v),
                  placeholder: "Why should the system remember this? What decision/action does it improve?",
                  rows: 3
                }),
                React.createElement(TextArea, {
                  label: "Global HOW (mechanism)",
                  value: project.global_context.how,
                  onChange: v => updateProject("global_context.how", v),
                  placeholder: "How will this be applied? (agents, prompts, workflows, guardrails)",
                  rows: 3
                }),
                React.createElement("div", { className: "space-y-4" },
                  React.createElement(TextInput, {
                    label: "WHERE – System",
                    value: project.global_context.where.system,
                    onChange: v => updateProject("global_context.where.system", v),
                    placeholder: "e.g., Teamcenter PLM, Salesforce, Gmail, Slack"
                  }),
                  React.createElement(TextInput, {
                    label: "WHERE – Channel",
                    value: project.global_context.where.channel,
                    onChange: v => updateProject("global_context.where.channel", v),
                    placeholder: "e.g., email, meeting, ticketing, docs"
                  }),
                  React.createElement(TextInput, {
                    label: "WHERE – Location (optional)",
                    value: project.global_context.where.location,
                    onChange: v => updateProject("global_context.where.location", v),
                    placeholder: "e.g., Cancun / Remote"
                  })
                )
              )
            ),

            React.createElement(Section, {
              title: "2) Upload files (artifacts)",
              subtitle: "Upload source files. The backend can convert these and attach the manifest metadata."
            },
              React.createElement("div", { className: "flex flex-col md:flex-row md:items-center gap-3" },
                React.createElement("input", {
                  type: "file",
                  multiple: true,
                  className: "block w-full text-sm text-slate-300 file:mr-4 file:rounded-xl file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-500",
                  onChange: (e) => addFiles(e.target.files)
                }),
                React.createElement("div", { className: "text-xs text-slate-400" },
                  "Tip: PDFs/images/audio are acceptable; treat extraction_method + confidence seriously."
                )
              ),

              React.createElement("div", { className: "mt-5" },
                project.artifacts.length === 0
                  ? React.createElement("div", { className: "text-sm text-slate-400" }, "No files uploaded yet.")
                  : React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3" },
                      project.artifacts.map(a =>
                        React.createElement("div", {
                          key: a.artifact_id,
                          className: `rounded-2xl border p-4 bg-slate-950/40 ${
                            (currentArtifact && currentArtifact.artifact_id === a.artifact_id) ? "border-blue-600" : "border-slate-800"
                          }`
                        },
                          React.createElement("div", { className: "flex items-start justify-between gap-3" },
                            React.createElement("div", null,
                              React.createElement("div", { className: "font-semibold" }, a.file.name),
                              React.createElement("div", { className: "mt-1 text-xs text-slate-400 mono" }, a.artifact_id),
                              React.createElement("div", { className: "mt-2 flex flex-wrap gap-2" },
                                React.createElement(Badge, null, a.file.mime_type),
                                React.createElement(Badge, null, `${Math.round(a.file.size_bytes/1024)} KB`),
                                React.createElement(Badge, null, a.quality.extraction_method)
                              )
                            ),
                            React.createElement("div", { className: "flex flex-col gap-2" },
                              React.createElement(PillButton, {
                                variant: "secondary",
                                onClick: () => setSelectedArtifactId(a.artifact_id)
                              }, "Select"),
                              React.createElement(PillButton, {
                                variant: "danger",
                                onClick: () => removeArtifact(a.artifact_id)
                              }, "Remove")
                            )
                          )
                        )
                      )
                    )
              )
            )
          );
        }

        function Step2_PerFile5W1H() {
          if (!currentArtifact) {
            return React.createElement("div", { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-6" },
              React.createElement("div", { className: "text-slate-300" }, "Upload at least one file in Step 1.")
            );
          }

          const a = currentArtifact;

          return React.createElement("div", { className: "space-y-6" },
            React.createElement(Section, {
              title: "3) File context: WHAT / WHERE / WHEN / WHY / HOW",
              subtitle: "Per-file context overrides global defaults. Aim for decision-grade specificity.",
              right: React.createElement(Badge, null, a.file.name)
            },
              React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4" },
                React.createElement(TextInput, {
                  label: "Source URI/path (optional but high value)",
                  value: a.source.uri,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.source.uri = v, x)),
                  placeholder: "e.g., drive://..., https://..., slack://..., local path"
                }),
                React.createElement(TextInput, {
                  label: "Origin system (required)",
                  value: a.source.origin_system,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.source.origin_system = v, x)),
                  placeholder: "e.g., Gmail, Zoom, Drive, Confluence, Jira"
                }),
                React.createElement(TextInput, {
                  label: "Author / Owner (attribution)",
                  value: a.source.author,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.source.author = v, x)),
                  placeholder: "Person or system that created the content"
                }),
                React.createElement(Select, {
                  label: "Confidentiality",
                  value: a.source.confidentiality,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.source.confidentiality = v, x)),
                  options: [
                    { value: "public", label: "public" },
                    { value: "internal", label: "internal" },
                    { value: "confidential", label: "confidential" },
                    { value: "restricted", label: "restricted" }
                  ]
                }),

                React.createElement(TextArea, {
                  label: "WHAT (what is in this file)",
                  value: a.context_5w1h.what,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.what = v, x)),
                  placeholder: "Summarize content, scope, and key subject(s).",
                  rows: 3
                }),
                React.createElement(TextArea, {
                  label: "WHY (why it matters / intended use)",
                  value: a.context_5w1h.why,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.why = v, x)),
                  placeholder: "What decision, workflow, or automation does this improve?",
                  rows: 3
                }),
                React.createElement(TextArea, {
                  label: "HOW (how it should be applied)",
                  value: a.context_5w1h.how,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.how = v, x)),
                  placeholder: "How should an agent use this? constraints, guardrails, triggers.",
                  rows: 3
                }),
                React.createElement("div", { className: "space-y-4" },
                  React.createElement(TextInput, {
                    label: "WHERE – System (required)",
                    value: a.context_5w1h.where.system,
                    onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.where.system = v, x)),
                    placeholder: "System / product / platform"
                  }),
                  React.createElement(TextInput, {
                    label: "WHERE – Channel",
                    value: a.context_5w1h.where.channel,
                    onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.where.channel = v, x)),
                    placeholder: "email / meeting / ticket / doc / code / spreadsheet"
                  }),
                  React.createElement(TextInput, {
                    label: "WHERE – Location (optional)",
                    value: a.context_5w1h.where.location,
                    onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.where.location = v, x)),
                    placeholder: "Physical location if relevant"
                  })
                ),

                React.createElement(TextInput, {
                  label: "WHEN – Start (ISO-8601)",
                  value: a.context_5w1h.when.start_iso,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.when.start_iso = v, x)),
                  placeholder: "e.g., 2026-02-09T10:00:00-05:00"
                }),
                React.createElement(TextInput, {
                  label: "WHEN – End (ISO-8601)",
                  value: a.context_5w1h.when.end_iso,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.when.end_iso = v, x)),
                  placeholder: "optional"
                }),
                React.createElement(TextInput, {
                  label: "Timezone",
                  value: a.context_5w1h.when.timezone,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.context_5w1h.when.timezone = v, x)),
                  placeholder: "e.g., America/Cancun"
                }),
                React.createElement(Select, {
                  label: "Extraction method",
                  value: a.quality.extraction_method,
                  onChange: v => updateArtifact(a.artifact_id, x => (x.quality.extraction_method = v, x)),
                  options: [
                    { value: "native_text", label: "native_text" },
                    { value: "ocr", label: "ocr" },
                    { value: "transcript", label: "transcript" },
                    { value: "manual", label: "manual" },
                    { value: "mixed", label: "mixed" }
                  ],
                  hint: "Backend can route different pipelines based on this."
                })
              )
            )
          );
        }

        function Step3_FactVsInference_7s() {
          if (!currentArtifact) {
            return React.createElement("div", { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-6" },
              React.createElement("div", { className: "text-slate-300" }, "Upload at least one file in Step 1.")
            );
          }

          const a = currentArtifact;

          return React.createElement("div", { className: "space-y-6" },
            React.createElement(Section, {
              title: "4) Fact vs inference split (Rule-of-7s)",
              subtitle: "Prevent memory poisoning: explicitly separate observations, claims, assumptions, and model inferences.",
              right: React.createElement(Badge, null, a.file.name)
            },
              React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4" },
                React.createElement(LimitedListEditor, {
                  title: "Observations (facts / extracted statements)",
                  subtitle: "Concrete items. No speculation.",
                  items: a.fact_inference_split.observations || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.fact_inference_split.observations = items, x)),
                  placeholder: "e.g., 'Client uses Teamcenter with custom data model X...'"
                }),
                React.createElement(LimitedListEditor, {
                  title: "Claims (assertions by someone)",
                  subtitle: "Track attribution separately via Author/Owner.",
                  items: a.fact_inference_split.claims || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.fact_inference_split.claims = items, x)),
                  placeholder: "e.g., 'This will reduce implementation cost by 80%...'"
                }),
                React.createElement(LimitedListEditor, {
                  title: "Assumptions (unstated dependencies)",
                  subtitle: "Items that must be true for the claims to hold.",
                  items: a.fact_inference_split.assumptions || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.fact_inference_split.assumptions = items, x)),
                  placeholder: "e.g., 'Access to customer schema export is available...'"
                }),
                React.createElement(LimitedListEditor, {
                  title: "Inferences (model-generated conclusions)",
                  subtitle: "Keep this separate; treat as low-trust until validated.",
                  items: a.fact_inference_split.inferences || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.fact_inference_split.inferences = items, x)),
                  placeholder: "e.g., 'Likely bottleneck is schema drift across deployments...'"
                })
              )
            ),

            React.createElement(Section, {
              title: "5) Causal layer capture (Events / Decisions / Tasks)",
              subtitle: "Encode what-changed-what. This is where GME-style reasoning compounds.",
              right: React.createElement(Badge, null, "7 max each")
            },
              React.createElement("div", { className: "grid grid-cols-1 gap-4" },
                React.createElement(LimitedListEditor, {
                  title: "Events",
                  subtitle: "Time-bounded changes with actors + inputs + outputs.",
                  items: a.gme_causal_layer.events || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.gme_causal_layer.events = items, x)),
                  fields: [
                    { key: "event_id", label: "event_id (optional)", placeholder: "evt_..." },
                    { key: "title", label: "title", placeholder: "What happened?" },
                    { key: "start_iso", label: "start_iso", placeholder: "2026-02-09T..." },
                    { key: "end_iso", label: "end_iso", placeholder: "optional" },
                    { key: "actors", label: "actors (comma-separated)", placeholder: "Person/Org/System" },
                    { key: "inputs", label: "inputs (comma-separated)", placeholder: "Artifacts/data used" },
                    { key: "outputs", label: "outputs (comma-separated)", placeholder: "Decisions/tasks/results" },
                    { key: "outcome", label: "outcome", placeholder: "Net effect / result" },
                    { key: "confidence", label: "confidence (0-1)", placeholder: "0.8" }
                  ],
                  objectTemplate: { event_id: "", title: "", start_iso: "", end_iso: "", actors: "", inputs: "", outputs: "", outcome: "", confidence: "0.8" }
                }),

                React.createElement(LimitedListEditor, {
                  title: "Decisions",
                  subtitle: "Decision statements with rationale + evidence refs.",
                  items: a.gme_causal_layer.decisions || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.gme_causal_layer.decisions = items, x)),
                  fields: [
                    { key: "decision_id", label: "decision_id (optional)", placeholder: "dec_..." },
                    { key: "statement", label: "decision statement", placeholder: "Decision made" },
                    { key: "owner", label: "owner", placeholder: "Who owns it" },
                    { key: "date_iso", label: "date_iso", placeholder: "2026-02-09" },
                    { key: "rationale", label: "rationale", placeholder: "Why this decision", type: "textarea" },
                    { key: "evidence_refs", label: "evidence_refs (comma-separated)", placeholder: "artifact_id:segment..." },
                    { key: "confidence", label: "confidence (0-1)", placeholder: "0.8" }
                  ],
                  objectTemplate: { decision_id: "", statement: "", owner: "", date_iso: "", rationale: "", evidence_refs: "", confidence: "0.8" }
                }),

                React.createElement(LimitedListEditor, {
                  title: "Tasks",
                  subtitle: "Implementation actions with owners + due dates + dependencies.",
                  items: a.gme_causal_layer.tasks || [],
                  onChange: items => updateArtifact(a.artifact_id, x => (x.gme_causal_layer.tasks = items, x)),
                  fields: [
                    { key: "task_id", label: "task_id (optional)", placeholder: "tsk_..." },
                    { key: "title", label: "title", placeholder: "Action" },
                    { key: "owner", label: "owner", placeholder: "Responsible" },
                    { key: "due_iso", label: "due_iso", placeholder: "2026-02-16" },
                    { key: "status", label: "status", placeholder: "planned/in_progress/done" },
                    { key: "dependencies", label: "dependencies (comma-separated)", placeholder: "tsk_..., art_..." }
                  ],
                  objectTemplate: { task_id: "", title: "", owner: "", due_iso: "", status: "planned", dependencies: "" }
                })
              )
            )
          );
        }

        function Step4_EntitiesAndRelations() {
          // Global entities/relations that can be referenced by artifacts/events later
          return React.createElement("div", { className: "space-y-6" },
            React.createElement(Section, {
              title: "6) Entities (people / orgs / systems / concepts)",
              subtitle: "Use stable IDs + aliases. This drives cross-file linking and causal reasoning."
            },
              React.createElement(LimitedListEditor, {
                title: "Entities",
                subtitle: "Max 7 for focus; add more via multiple manifests if needed.",
                items: project.entities || [],
                onChange: items => setProject(prev => ({ ...prev, entities: items })),
                fields: [
                  { key: "entity_id", label: "entity_id (optional)", placeholder: "ent_..." },
                  { key: "type", label: "type", placeholder: "person/org/system/concept" },
                  { key: "name", label: "name", placeholder: "Canonical name" },
                  { key: "aliases", label: "aliases (comma-separated)", placeholder: "nicknames, abbreviations" },
                  { key: "attributes", label: "attributes (JSON text)", placeholder: '{"role":"..."}' },
                  { key: "confidence", label: "confidence (0-1)", placeholder: "0.9" }
                ],
                objectTemplate: { entity_id: "", type: "", name: "", aliases: "", attributes: "{}", confidence: "0.9" }
              })
            ),

            React.createElement(Section, {
              title: "7) Relations (typed edges)",
              subtitle: "Encode dependencies and influence: depends_on, owns, supports, contradicts, caused_by, etc."
            },
              React.createElement(LimitedListEditor, {
                title: "Relations",
                subtitle: "Keep relation types consistent. Treat evidence_refs as pointers to artifacts/segments.",
                items: project.relations || [],
                onChange: items => setProject(prev => ({ ...prev, relations: items })),
                fields: [
                  { key: "relation_id", label: "relation_id (optional)", placeholder: "rel_..." },
                  { key: "type", label: "type", placeholder: "depends_on/owns/supports/contradicts/caused_by" },
                  { key: "from_ref", label: "from_ref", placeholder: "entity_id / artifact_id / event_id" },
                  { key: "to_ref", label: "to_ref", placeholder: "entity_id / artifact_id / event_id" },
                  { key: "evidence_refs", label: "evidence_refs (comma-separated)", placeholder: "art_x:page2, ..." },
                  { key: "confidence", label: "confidence (0-1)", placeholder: "0.8" }
                ],
                objectTemplate: { relation_id: "", type: "", from_ref: "", to_ref: "", evidence_refs: "", confidence: "0.8" }
              })
            )
          );
        }

        function Step5_ReviewAndExport() {
          return React.createElement("div", { className: "space-y-6" },
            React.createElement(Section, {
              title: "8) Review gaps (blocking) and export",
              subtitle: "Export the manifest and attach it to backend conversion output. The JSON is designed to be manually uploaded downstream."
            },
              readiness.missing.length
                ? React.createElement("div", { className: "rounded-xl border border-rose-900 bg-rose-950/30 p-4" },
                    React.createElement("div", { className: "font-semibold text-rose-200" }, "Gaps to fix"),
                    React.createElement("ul", { className: "mt-2 list-disc list-inside text-sm text-rose-100/90 space-y-1" },
                      readiness.missing.slice(0, 50).map((m, i) => React.createElement("li", { key: i }, m))
                    ),
                    readiness.missing.length > 50
                      ? React.createElement("div", { className: "mt-2 text-xs text-rose-200/80" }, `+ ${readiness.missing.length - 50} more...`)
                      : null
                  )
                : React.createElement("div", { className: "rounded-xl border border-emerald-900 bg-emerald-950/30 p-4" },
                    React.createElement("div", { className: "font-semibold text-emerald-200" }, "Ready for export"),
                    React.createElement("div", { className: "mt-1 text-sm text-emerald-100/90" },
                      "No blocking gaps detected. Export now and hand to backend conversion pipeline."
                    )
                  ),

              React.createElement("div", { className: "mt-4 grid grid-cols-1 md:grid-cols-2 gap-4" },
                React.createElement(TextArea, {
                  label: "Reviewer notes (optional)",
                  value: project.review.notes,
                  onChange: v => updateProject("review.notes", v),
                  placeholder: "Any critical caveats, constraints, or instructions for the backend pipeline.",
                  rows: 4
                }),
                React.createElement("div", { className: "rounded-xl border border-slate-800 bg-slate-950/40 p-4" },
                  React.createElement("div", { className: "text-sm font-semibold" }, "Export actions"),
                  React.createElement("div", { className: "mt-2 text-sm text-slate-300" },
                    "Manifest (.json): full project + file metadata. Records (.jsonl): atomic stubs for ingestion."
                  ),
                  React.createElement("div", { className: "mt-3 flex flex-wrap gap-2" },
                    React.createElement(PillButton, { variant: "primary", onClick: exportManifest }, "Download Manifest"),
                    React.createElement(PillButton, { variant: "secondary", onClick: exportJsonlStubs }, "Download JSONL Records")
                  )
                )
              )
            ),

            React.createElement(Section, {
              title: "9) Manifest preview (read-only)",
              subtitle: "Sanity check before handing off. This is the file you manually upload downstream."
            },
              React.createElement("pre", { className: "mono text-xs overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4 max-h-[520px]" },
                safeJsonStringify(project)
              )
            )
          );
        }

        const main = React.createElement("div", { className: "mx-auto max-w-6xl px-4 py-8" },
          React.createElement("div", { className: "flex flex-col md:flex-row gap-6" },

            // Left nav
            React.createElement("div", { className: "md:w-72 space-y-3" },
              React.createElement("div", { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-4" },
                React.createElement("div", { className: "text-sm font-semibold" }, "Workflow"),
                React.createElement("div", { className: "mt-3 space-y-2" },
                  [
                    { n: 1, t: "Project + Files" },
                    { n: 2, t: "Per-file 5W1H" },
                    { n: 3, t: "Fact/Inference + Causal" },
                    { n: 4, t: "Entities + Relations" },
                    { n: 5, t: "Review + Export" }
                  ].map(s =>
                    React.createElement("button", {
                      key: s.n,
                      className: `w-full text-left rounded-xl border px-3 py-2 text-sm transition ${
                        step === s.n ? "border-blue-600 bg-blue-600/10" : "border-slate-800 bg-slate-950/30 hover:bg-slate-950/60"
                      }`,
                      onClick: () => setStep(s.n)
                    },
                      React.createElement("div", { className: "flex items-center justify-between" },
                        React.createElement("span", null, `${s.n}. ${s.t}`),
                        step === s.n ? React.createElement(Badge, null, "Active") : null
                      )
                    )
                  )
                )
              ),

              React.createElement("div", { className: "rounded-2xl border border-slate-800 bg-slate-900/40 p-4" },
                React.createElement("div", { className: "text-sm font-semibold" }, "Selected file"),
                currentArtifact
                  ? React.createElement("div", { className: "mt-2" },
                      React.createElement("div", { className: "text-sm" }, currentArtifact.file.name),
                      React.createElement("div", { className: "mt-1 text-xs text-slate-400 mono" }, currentArtifact.artifact_id),
                      React.createElement("div", { className: "mt-2 text-xs text-slate-400" },
                        "Switch files in Step 1 (Select)."
                      )
                    )
                  : React.createElement("div", { className: "mt-2 text-sm text-slate-400" }, "None selected.")
              )
            ),

            // Right content
            React.createElement("div", { className: "flex-1 space-y-6" },
              step === 1 ? React.createElement(Step1_ProjectAndFiles)
              : step === 2 ? React.createElement(Step2_PerFile5W1H)
              : step === 3 ? React.createElement(Step3_FactVsInference_7s)
              : step === 4 ? React.createElement(Step4_EntitiesAndRelations)
              : React.createElement(Step5_ReviewAndExport),

              React.createElement("div", { className: "flex items-center justify-between" },
                React.createElement(PillButton, { variant: "secondary", onClick: prev, disabled: step === 1 }, "Back"),
                React.createElement("div", { className: "flex items-center gap-2" },
                  React.createElement(PillButton, { variant: "secondary", onClick: () => setStep(1) }, "Jump to Step 1"),
                  React.createElement(PillButton, { variant: "primary", onClick: next, disabled: step === totalSteps }, "Next")
                )
              )
            )
          )
        );

        return React.createElement(React.Fragment, null, topBar, main);
      }

      ReactDOM.createRoot(document.getElementById("root")).render(React.createElement(App));
    </script>
  </body>
</html>
```



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)