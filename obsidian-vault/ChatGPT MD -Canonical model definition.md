# Canonical model definition

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 9/15/2025 19:31:40  
**Updated:** 10/30/2025 17:41:23  
**Exported:** 3/19/2026 17:10:03  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/46be79c3-5a20-8325-af6e-081a5ab0f814](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/46be79c3-5a20-8325-af6e-081a5ab0f814)  

## Prompt:
what is Canonical Model

## Response:
A **Canonical Model** is a standardized, simplified representation of data, concepts, or processes that serves as a **“single source of truth”** for integration and communication across systems, teams, or domains.

It’s called _canonical_ (from the Greek _kanon_, meaning "rule" or "standard") because it establishes a **common language or schema** that all parties agree to use, regardless of the complexity or diversity of underlying systems.

* * *

### Key Characteristics:

*   **Neutral & Unified**: Removes system-specific quirks and creates a platform-independent structure.
*   **Abstracted**: Focuses on core concepts (e.g., “Customer,” “Order,” “Invoice”) rather than implementation details.
*   **Reusable**: Designed so multiple applications or services can map to it.
*   **Stable**: Changes infrequently compared to individual system models, so it provides long-term consistency.

* * *

### Where It’s Used:

1.  **Data Integration & Messaging**
    *   In enterprise integration (EAI, SOA, ESB), a canonical model allows different applications to exchange data using a consistent format.
    *   Example: Multiple CRMs and ERPs all map their “Customer” object into the canonical “Customer” model for smooth communication.
2.  **Knowledge Representation**
    *   In semantic models and ontologies, canonical models define standard entities and relationships.
    *   Example: FIBO (Financial Industry Business Ontology) acts as a canonical model for finance.
3.  **APIs & Microservices**
    *   Prevents a "spaghetti" of point-to-point translations by standardizing request/response payloads.
4.  **AI/ML & Data Lakes**
    *   Provides a clean, normalized schema for training models or analyzing large datasets.

* * *

### Example:

Imagine three systems that define a **Customer** differently:

*   CRM: `FirstName, LastName, Phone`
*   E-commerce: `FullName, Email`
*   Support Desk: `CustomerID, Contact`

A **Canonical Customer Model** might be:

```
Customer {
   CustomerID
   FullName
   FirstName
   LastName
   Email
   Phone
}
```

Each system maps its fields into this model. Now data exchange is seamless.

* * *

✅ **Long-term ROI Insight**:  
The canonical model requires upfront investment (design, mapping, governance), but it **pays off exponentially** by reducing translation complexity, data mismatches, and integration costs over time. Instead of building `n²` translations between systems, each system only needs **one translation**—to/from the canonical model. This is a compounding efficiency gain.

* * *

Do you want me to show you how a **canonical model** would look specifically for **Gigaton’s ecosystem** (real estate, AI sales agents, property management, wellness, etc.), so you have a master schema to unify all your projects?

## Prompt:
yes

## Response:
awesome—here’s a practical, ROI-oriented **Canonical Model** for Gigaton’s ecosystem that unifies real estate, agentic sales, interactive experiences, wellness/marketplace, and finance. It’s designed to minimize n² integrations, speed time-to-revenue, and keep data/AI training clean and reusable.

Canonical Model (Gigaton)
=========================

0) Conventions
--------------

*   IDs: `ulid` (string), globally unique (e.g., `CUS_01H…`), human-readable prefixes.
*   Timestamps: `created_at`, `updated_at`, `deleted_at` (nullable).
*   Status enums use `snake_case` (e.g., `active`, `archived`).
*   PII isolation: store sensitive fields in a dedicated vault table/secret store and reference by token.
*   Multitenancy: every record includes `tenant_id` (Gigaton brand/client).

* * *

1) Identity & Access (foundation)
---------------------------------

**Party** (supertype for people & orgs)

*   `party_id`, `tenant_id`, `party_type` (`person|organization`), `display_name`, `tags[]`

**Person**

*   `party_id (FK Party)`, `first_name`, `last_name`, `dob?`, `gender?`

**Organization**

*   `party_id (FK Party)`, `legal_name`, `tax_id?`, `industry?`, `size_bucket?`

**Account** (login/app profile, CRM record)

*   `account_id`, `party_id`, `account_origin` (`crm|portal|agent|import`), `lifecycle_stage` (`lead|mql|sql|customer|partner|affiliate`)

**ContactPoint**

*   `contact_id`, `party_id`, `type` (`email|phone|whatsapp|sms|social|address`), `value`, `is_primary`

**Consent**

*   `consent_id`, `party_id`, `channel` (`email|sms|voice|whatsapp|ads|cookies`), `status` (`granted|revoked|pending`), `source`, `scope`, `jurisdiction`

* * *

2) Geography & Assets
---------------------

**Location**

*   `location_id`, `type` (`street_address|geo_point|polygon`), `address*`, `lat`, `lng`, `country_code`, `place_id?`

**DigitalAsset** (files: Matterport, images, video, docs)

*   `asset_id`, `owner_party_id`, `kind` (`matterport|image|video|pdf|mesh|lidar|audio`), `uri`, `checksum`, `width?`, `height?`, `duration_s?`, `license`, `visibility` (`public|private|shared`)

**ScanSession** (Matterport/LiDAR capture)

*   `scan_id`, `property_id?`, `captured_by_party_id`, `tech` (`matterport|lidar|photogrammetry`), `scan_purpose` (`listing|training|marketing|archival|mapping`), `asset_id (FK DigitalAsset)`, `resolution`, `coverage_area_m2?`, `water_env` (`surface|underwater|cave`), `quality_score`

* * *

3) Real Estate Domain
---------------------

**Property**

*   `property_id`, `owner_party_id?`, `manager_party_id?`, `location_id`, `property_type` (`condo|house|villa|commercial|land`), `beds?`, `baths?`, `area_m2?`, `amenities[]`, `year_built?`, `hoa_fees_mo?`, `valuation_estimate?`

**Listing**

*   `listing_id`, `property_id`, `listing_type` (`sale|rent|airbnb|pre_sale`), `status` (`draft|active|under_contract|sold|withdrawn|expired`), `price`, `currency`, `available_from?`, `mls_id?`, `channels[]` (`portal_x`, `fb`, `ig`, `seo`, `walk-in`)

**Booking/Stay** (for rentals/PM)

*   `booking_id`, `property_id`, `guest_party_id`, `channel` (`airbnb|direct|partner`), `check_in`, `check_out`, `payout_account_id`, `fees_breakdown{}`, `status`

* * *

4) Commerce, Contracts, & Finance
---------------------------------

**Product** (sellable item: scan, session, subscription, package)

*   `product_id`, `category` (`scan|experience|session|subscription|service|hardware`), `name`, `uom`, `base_price`, `tax_code`, `active`

**PricePlan** (tiers)

*   `price_id`, `product_id`, `currency`, `billing_cycle` (`one_time|monthly|annual|per_use`), `unit_price`, `min_qty?`, `max_qty?`

**Quote/Order**

*   `order_id`, `buyer_party_id`, `seller_party_id (Gigaton/brand)`, `status` (`draft|sent|accepted|fulfilled|canceled`), `line_items[] {product_id, qty, unit_price, metadata}`, `totals{subtotal,tax,discount,grand_total}`

**Contract**

*   `contract_id`, `order_id?`, `effective_at`, `term_months`, `auto_renew`, `sla_tier`, `termination_rights`, `doc_asset_id`

**Invoice**

*   `invoice_id`, `order_id`, `status` (`open|paid|void|overdue`), `amount_due`, `due_date`, `payments_applied[]`

**Payment**

*   `payment_id`, `invoice_id`, `provider` (`stripe|bank|cash`), `amount`, `currency`, `status` (`authorized|captured|failed|refunded`), `txn_ref`

**Affiliate**

*   `affiliate_id`, `party_id`, `program_id`, `payout_terms`, `status`; **AttributionEvent**: `click_id`, `affiliate_id`, `campaign_id`, `source`, `utm*`, `attributed_order_id?`

**Payout**

*   `payout_id`, `beneficiary_party_id`, `payout_account_id`, `amount`, `currency`, `status`, `period_start`, `period_end`

* * *

5) Engagement: Sales, Marketing, Support
----------------------------------------

**Campaign**

*   `campaign_id`, `objective` (`lead_gen|retarget|brand|upsell`), `budget`, `start_at`, `end_at`, `channels[]`

**Lead**

*   `lead_id`, `account_id?`, `source` (`ads|referral|walk_in|portal|whatsapp`), `interest` (`buy|sell|rent|scan|vibe|training`), `score`, `owner_user_id`, `status` (`new|working|nurturing|qualified|unqualified|converted`)

**Conversation** (omnichannel: voice/SMS/WA/webchat)

*   `conversation_id`, `participants[] (party_ids)`, `channel` (`voice|sms|whatsapp|web|email`), `status`;  
    **Message**: `message_id`, `conversation_id`, `direction` (`inbound|outbound`), `text`, `audio_asset_id?`, `metadata (twilio_sid, call_duration_s, sentiment?)`

**Task/Ticket**

*   `task_id`, `related_type/id` (Lead/Order/Property), `type` (`follow_up|site_visit|support|scan`), `priority`, `due_at`, `assignee_user_id`, `status`

**EventAttendance** (open house, scan day, festival)

*   `attendance_id`, `event_id`, `party_id`, `role` (`host|guest|crew`), `checkin_at`

* * *

6) Interactive Experiences (IE) & Training
------------------------------------------

**Experience** (interactive guided flows, virtual tours, AI demo journeys)

*   `experience_id`, `title`, `experience_type` (`tour|sales_play|training|onboarding`), `target_domain` (`real_estate|wellness|dive|venue`), `status`, `primary_asset_id?`, `steps[]`

**Session** (user run of an Experience)

*   `session_id`, `experience_id`, `started_by_party_id`, `started_at`, `completed_at?`, `outcome` (`converted|qualified|abandoned`), `captures{answers, clicks, dwell_time_s}`

**Curriculum** (for PADI/SSI/wellness training)

*   `curriculum_id`, `title`, `level`, `modules[]`, `cert_body?`;  
    **TrainingRecord**: `record_id`, `party_id`, `curriculum_id`, `status`, `score?`, `evidence_asset_id?`

* * *

7) Wellness / Marketplace (Vibe)
--------------------------------

**ProviderProfile**

*   `provider_id (party_id)`, `modalities[]`, `credentials[]`, `bio`, `availability_calendar_id`, `hourly_rate`, `rating_avg`, `review_count`

**ServiceOffering**

*   `offering_id`, `provider_id`, `category` (`massage|breathwork|coaching`), `duration_min`, `price`, `location_type` (`in_person|virtual|on_site`)

**Appointment**

*   `appointment_id`, `offering_id`, `client_party_id`, `start_at`, `end_at`, `status`, `payment_policy`

* * *

8) Governance & Observability
-----------------------------

**DataLineage**

*   `lineage_id`, `entity_type/id`, `source_system`, `ingested_at`, `transform_version`, `confidence_score`

**ModelRegistry** (AI/SLM/LLM used in automations)

*   `model_id`, `name`, `version`, `provider`, `cost_per_1k_tokens`, `use_cases[]`, `eval_scores{}`

**Policy**

*   `policy_id`, `scope` (`consent|privacy|retention|ai_ethical`), `rule`, `effective_at`

* * *

9) Canonical Events (for ESB/Kafka/NATS or webhook bus)
-------------------------------------------------------

*   `party.created/updated`
*   `lead.created/updated/scored`
*   `conversation.started/message.sent/call.ended`
*   `property.created/listing.published/status.changed`
*   `scan.completed/asset.ingested`
*   `order.created/contract.signed/invoice.issued/payment.captured`
*   `experience.session.started/completed`
*   `affiliate.attributed/payout.processed`

**Event envelope (example):**

```
{
  "event_id": "EVT_01H…",
  "event_type": "order.created",
  "occurred_at": "2025-09-15T19:07:00Z",
  "tenant_id": "TEN_gigaton",
  "actor_party_id": "PTY_…",
  "data": { "order_id": "ORD_…", "totals": { "grand_total": 1499.00, "currency": "USD" } },
  "source_system": "sales-portal",
  "schema_version": "1.0.0"
}
```

* * *

10) Example Canonical Payloads
------------------------------

### Customer/Account

```
{
  "party": {
    "party_id": "PTY_01H…",
    "party_type": "person",
    "display_name": "Elisabeth Girard"
  },
  "person": { "first_name": "Elisabeth", "last_name": "Girard" },
  "account": {
    "account_id": "ACC_01H…",
    "lifecycle_stage": "customer",
    "account_origin": "portal"
  },
  "contacts": [
    {"type": "email", "value": "elisabeth@example.com", "is_primary": true},
    {"type": "whatsapp", "value": "+52999…"}
  ],
  "consents": [{"channel": "whatsapp", "status": "granted", "jurisdiction": "MX"}]
}
```

### Property + Listing

```
{
  "property": {
    "property_id": "PRP_01H…",
    "property_type": "condo",
    "location_id": "LOC_01H…",
    "beds": 2, "baths": 2, "area_m2": 110,
    "amenities": ["pool","gym","beach_access"]
  },
  "listing": {
    "listing_id": "LST_01H…",
    "listing_type": "sale",
    "status": "active",
    "price": 395000, "currency": "USD",
    "channels": ["portal_x","seo","ig"]
  }
}
```

### Scan / Digital Asset

```
{
  "scan": {
    "scan_id": "SCN_01H…",
    "property_id": "PRP_01H…",
    "tech": "matterport",
    "scan_purpose": "listing",
    "asset_id": "AST_01H…",
    "resolution": "4k",
    "coverage_area_m2": 120,
    "quality_score": 0.93
  }
}
```

### Conversation Message (Twilio)

```
{
  "message": {
    "message_id": "MSG_01H…",
    "conversation_id": "CON_01H…",
    "channel": "whatsapp",
    "direction": "outbound",
    "text": "Hi! Would you like a virtual tour?",
    "metadata": { "twilio_sid": "SMxxxxxxxx", "template": "tour_invite_v1" }
  }
}
```

* * *

11) Core KPI Layer (computed views)
-----------------------------------

*   **Marketing**: `lead_to_sql_rate`, `cac_blended`, `attribution_share_by_channel`, `affiliate_roas`.
*   **Sales**: `sql_to_win_rate`, `avg_sales_cycle_days`, `avg_deal_size`, `pipeline_coverage`.
*   **Property**: `listing_time_to_contract`, `scan_to_listing_ratio`, `scan_quality_to_conversion_corr`.
*   **PM/Bookings**: `occupancy_rate`, `revpar`, `avg_length_of_stay`, `owner_payout_margin`.
*   **IE/Training**: `experience_completion_rate`, `session_to_lead_rate`, `training_cert_rate`.
*   **Finance**: `net_revenue`, `gross_margin`, `working_capital_days`, `mrr|arr`, `churn`, `ltv:cac`.

_(We can materialize these as SQL views over the canonical tables; names like `vw_sales_funnel`, `vw_property_performance`, `vw_finance_mrr`.)_

* * *

12) Mapping & Integration Guidelines
------------------------------------

*   Each source system maps once to the canonical schema (no point-to-point):
    *   **Twilio** → `Conversation/Message` (+call metrics).
    *   **Matterport** → `ScanSession/DigitalAsset` (+Property linkage).
    *   **Stripe** → `Invoice/Payment/Payout`.
    *   **Meta/Google Ads** → `Lead/Campaign/AttributionEvent`.
    *   **Airbnb/Channel Manager** → `Booking/Stay`.
    *   **CRM** → `Account/Lead/Task`.
*   Use **Change Data Capture** (CDC) or webhooks to publish **Canonical Events**.
*   Version schemas with SemVer; deprecate fields with clear timelines.
*   Validate via JSON Schema; enforce PII/consent policies at the bus.

* * *

13) Why this maximizes ROI (Gigaton lens)
-----------------------------------------

*   **Compounding efficiency**: Every new system integrates once → marginal integration cost approaches zero as the ecosystem grows.
*   **Faster GTM**: New products (e.g., Vibe sessions, scan packages) reuse `Product/PricePlan/Order`—no re-plumbing.
*   **Better AI**: Clean, stable semantics drive higher model accuracy and lower feature engineering costs.
*   **Monetization levers**: Clear attribution + payout + contract data → predictable partner economics and M&A-ready metrics.

* * *

14) Next quick wins (suggested)
-------------------------------

1.  Stand up the **Party/Account/ContactPoint/Consent** core + **Conversation/Message** for Twilio.
2.  Add **Property/Listing** + **ScanSession/DigitalAsset** for Matterport flows.
3.  Layer **Order/Invoice/Payment** + **Affiliate/Payout**.
4.  Materialize KPIs (`vw_*`) and wire dashboards.

If you want, I can drop this as a **JSON Schema bundle** or **SQL DDL + KPI views** so your team can load it directly into your warehouse.

## Prompt:
What is the KG approach as it relates to data modeling

## Response:
Great question. The **Knowledge Graph (KG) approach** to data modeling is fundamentally different from traditional relational or canonical data modeling—it’s about **representing entities and their relationships in a flexible, semantically rich graph structure** rather than in rigid tables or fixed schemas.

* * *

🔑 Core Principles of the KG Approach
-------------------------------------

1.  **Entity–Relationship Focused (Nodes & Edges)**
    *   Instead of tables and joins, data is modeled as **nodes (entities)** and **edges (relationships)**.
    *   Example:
        *   Node: `Customer: Elisabeth Girard`
        *   Node: `Property: 123 Beach Ave Condo`
        *   Edge: `(Elisabeth Girard) —owns→ (123 Beach Ave Condo)`
2.  **Semantics & Ontologies**
    *   Entities and relationships are typed using **ontologies** (formal vocabularies).
    *   This enforces meaning, not just structure.
    *   Example: `owns` is not just a string—it belongs to an ontology that defines ownership.
3.  **Flexible Schema (Schema-Late)**
    *   You don’t need to predefine all columns/fields. You can add new entity types and relationships as the domain evolves.
    *   This makes KGs **future-proof** for rapidly evolving ecosystems (like Gigaton).
4.  **Context & Linking**
    *   Knowledge graphs allow linking across domains and external sources.
    *   Example: Linking your canonical `Property` node to **Wikidata** for regional context or to **OpenStreetMap** for geospatial metadata.
5.  **Reasoning & Inference**
    *   KGs support logic-based inference: if A → B and B → C, then A → C.
    *   Example: If a customer is an **affiliate**, and an affiliate is tied to a **payout**, you can infer which **customers** should trigger payouts without hard-coded rules.

* * *

⚖️ KG vs Canonical Model
------------------------

| Aspect | Canonical Model | Knowledge Graph |
| --- | --- | --- |
| **Purpose** | Standardize integration, reduce n² mappings | Represent knowledge & meaning, enable reasoning |
| **Structure** | Rigid schema (tables/objects) | Flexible graph (nodes/edges) |
| **Semantics** | Mostly implicit (column names, docs) | Explicit (ontologies, RDF/OWL, SHACL) |
| **Change handling** | Schema evolution painful | Add new nodes/edges with minimal disruption |
| **Querying** | SQL, joins | GraphQL/SPARQL, traversals |
| **Best for** | Transactional workflows, API payloads, reporting | Cross-domain reasoning, discovery, recommendations, context enrichment |

* * *

📍 Example: Gigaton KG
----------------------

Canonical Model example:

```
{
  "property": { "property_id": "PRP_01H", "beds": 2, "baths": 2 },
  "listing": { "listing_id": "LST_01H", "status": "active" },
  "account": { "account_id": "ACC_01H", "party_id": "PTY_01H" }
}
```

Knowledge Graph version (triple statements):

*   `(Property:PRP_01H) —hasListing→ (Listing:LST_01H)`
*   `(Listing:LST_01H) —status→ ("active")`
*   `(Account:ACC_01H) —belongsTo→ (Party:PTY_01H)`
*   `(Party:PTY_01H) —isOwnerOf→ (Property:PRP_01H)`

Now you can **traverse** queries like:  
_"Show me all Parties who own an active Listing in Playa del Carmen that has more than 2 bedrooms and was captured via Matterport scans."_  
This is far simpler in a KG than in rigid SQL joins across 10+ canonical tables.

* * *

✅ Why KG Matters for Gigaton
----------------------------

*   **Unifies domains**: Real estate, wellness, agentic sales, Matterport scans → all become connected concepts, not siloed tables.
*   **Future-proof**: You can easily model new verticals (e.g., diving, training, affiliate networks) without schema redesign.
*   **AI leverage**: Graph embeddings + LLMs + KG = contextual reasoning (recommendations, matching, fraud detection, conversational AI grounding).
*   **M&A/exit readiness**: Buyers (e.g., Matterport, CoStar) value data networks. A KG makes your data portable and interoperable.

* * *

👉 In short:

*   **Canonical Model = standard API contract for transactions.**
*   **Knowledge Graph = semantic web of meaning for discovery, reasoning, and AI.**  
    They’re **complementary**: use the canonical model for clean operations and the KG to **connect, enrich, and evolve knowledge across the ecosystem**.

* * *

Do you want me to **map the Canonical Model I drafted into a KG ontology** (like FIBO-style triples) so you see how the two co-exist in Gigaton? That would give you a blueprint for **transaction + knowledge layers**.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)