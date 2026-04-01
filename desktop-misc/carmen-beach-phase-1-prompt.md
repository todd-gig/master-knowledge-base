# Carmen Beach Properties — Phase 1 Claude Code Prompt

## Optional execution constraints assumed
- Reject shallow scaffolding. Prefer working vertical slices with real schema, routes, services, and admin screens over placeholder files.
- Before writing code, inspect the repository and preserve current architectural patterns where sensible. Since the repo is effectively empty, establish clean conventions that support future phases without overengineering.

## Prompt

You are a senior full-stack architect and systems designer.

Your task is to build a production-grade monorepo for a real estate + tourism platform called:

**Carmen Beach Properties**

This is **not** a simple listing site.

This is a vertically integrated system designed to:
- acquire property inventory
- generate demand via SEO + affiliates
- capture and convert leads
- support bookings (short-term rental optional)
- optimize revenue (occupancy vs pricing)
- track full-funnel attribution and user behavior

You are starting from:
- empty repository
- no tech stack defined
- no structure

You must define **everything** and scaffold the entire system.

---

## Primary business objectives

1. Maximize property exposure and conversion
2. Capture and track all user interactions
3. Enable affiliate-driven growth
4. Support both:
   - property sales
   - short-term rentals
5. Build reusable infrastructure for scaling geographically

---

## Required system components

### 1. Public Web App (Primary Acquisition Layer)
- SEO-optimized property listings
- Search + filters (location, price, amenities, proximity)
- Property detail pages:
  - media (images, video, drone, Matterport-ready)
  - amenities
  - proximity (beach, attractions)
- Lead capture:
  - inquiry forms
  - WhatsApp integration (stub)
- Tracking:
  - session tracking
  - UTM attribution

### 2. Admin Portal (Supply + Ops Layer)
- CRUD for:
  - properties
  - property owners
  - media assets
- Bulk import capability (CSV-ready)
- Status management:
  - active / inactive / draft
- Pricing + availability fields

### 3. Affiliate System (Growth Layer)
- Unique tracking links per partner
- Attribution via:
  - UTM parameters
  - session tracking
- Commission-ready structure (no payouts yet)

### 4. Data + Analytics Layer (Critical)
Implement structured tracking based on this schema:
- locale
- timezone
- geo (country, region, city, lat, lon)
- device (type, os, browser)
- traffic (utm_source, utm_medium, utm_campaign, etc.)
- session_id
- request_id

This must be:
- captured on every request
- stored in database
- accessible for analytics queries

### 5. API Layer
- REST or GraphQL (choose best)
- Must support:
  - listings
  - search
  - inquiries
  - admin actions
  - tracking ingestion

### 6. Database Design
Core entities:
- Property
- PropertyOwner
- Listing
- MediaAsset
- Inquiry
- Affiliate
- Session
- Event (tracking)

Relationships must be normalized and scalable.

---

## Tech stack requirements

Use modern, scalable, production-grade tools.

Preferred direction:

**Frontend**
- Next.js (App Router)
- TypeScript
- Tailwind

**Backend**
- Next.js API routes OR separate Node service

**Database**
- PostgreSQL

**ORM**
- Prisma

**Analytics**
- First-party event tracking system (no external dependency required)

**Deployment**
- Must be deployable to Google Cloud (Cloud Run compatible)

---

## Repo structure (mandatory)

Use monorepo structure:

/apps
  /web        (public site)
  /admin      (admin portal)
  /api        (if separate)

/packages
  /ui         (shared components)
  /db         (Prisma schema + client)
  /utils      (shared logic)
  /tracking   (event system)

/infra
  (deployment configs)

/scripts
  (setup + seed)

---

## Core features to implement first

Priority order:
1. Project scaffolding
2. Database schema (Prisma)
3. Property listing + detail pages
4. Admin CRUD for properties
5. Inquiry form (lead capture)
6. Tracking system (sessions + events)
7. Basic affiliate tracking

---

## Non-functional requirements

- Clean architecture
- Strong typing everywhere
- Modular and extensible
- SEO-first rendering
- Fast load times
- Mobile-first UX

---

## Output requirements

You must:
1. Initialize full repo structure
2. Generate all config files:
   - package.json
   - tsconfig
   - eslint
   - prettier
3. Create Prisma schema
4. Scaffold Next.js apps
5. Implement first working vertical slice:
   - homepage
   - listings page
   - property detail page
6. Implement basic admin panel
7. Implement API routes
8. Implement tracking middleware

Do **not** explain. Build.

Proceed step-by-step and output code incrementally.
