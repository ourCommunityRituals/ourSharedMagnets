# CLAUDE.md — OurSharedMagnets (OSM)

> **Session protocol**: Read this file → Read OCR-docs `docs/VISION.md` → Understand OSM's role in the OCR product line → Execute the task.

---

## What this repo is

OurSharedMagnets is the developer and franchise layer for OurCommunityRituals. API and white label support. Postman collections. Newman CI. Ritual execution skill files.

OSM is the institutional knowledge of the founding team delivered to corridor operators. When a new corridor wants to run what Blue Island runs, OSM is how they learn.

This repo is currently documentation-as-code. Developer tooling and franchise documentation will be added as the platform matures.

---

## Product identity

| Field | Value |
|-------|-------|
| Code | OSM |
| Full name | OurSharedMagnets |
| Type | Developer and franchise layer |
| Data model | API documentation, Postman collections, runbooks |
| Dependencies | OSE (platform), OA (deployment), all products (franchise knowledge) |
| Status | Documentation-as-code |

---

## What OSM owns

- API documentation and developer guides
- Postman collections for all OSE endpoints
- Newman CI integration for API testing
- Ritual execution skill files — how to run an activation
- Franchise documentation — the playbook for new corridor operators
- White label API support documentation
- Institutional knowledge capture and transfer

## What OSM does NOT own

- Platform infrastructure (OSE)
- Game night format (OSG)
- Client deployment and forking (OA)
- Music curation (OW)
- Consulting relationships (OSP)
- Analytics and intelligence (OER)

---

## Key distinction

OSM is knowledge transfer. OA is deployment execution. OSM tells you how. OA sets up the environment. They work together but own different things.

---

## Architectural boundaries

- **OSE is the platform.** OSM documents its APIs, does not build them.
- **OA handles deployment.** OSM documents the process; OA executes the fork, environment setup, and onboarding.
- **OSM serves corridor operators.** The audience is the person running activations in a new geography, not the end user at the event.
- **Postman/Newman collections mirror OSE routes.** Every OSE API endpoint has a corresponding Postman request. Newman runs them in CI.

---

## Links to other products

Every link that carries data, code or rules between OCR products is listed in OCR-docs `ocr-docs-brain/data-edges.yaml`. **A data link that is not listed there is not allowed.**

- **This repo's data links today:** E4, OSM to ourEventRings: written in the OER boundary doc, no code yet (`contract_only`).
- **Shared links every spoke has:** C1 (the hub's design system, pinned in `.ocr-hub-ref`) and G1 (the brain's rules and checks).
- **Before writing code that sends or reads another product's data:** add the link to `data-edges.yaml` in an OCR-docs PR first, with its privacy class and what enforces it. The field-level rules stay in OCR-docs `docs/architecture/OCR_ARCHITECTURE_oerAggregationBoundary.md`.

Product id in that file: `osm`.

---

## DAC compliance

| File | Purpose | Status |
|------|---------|--------|
| CLAUDE.md | Session protocol | Present |
| README.md | Public-facing description | Present |
| SKILL.md | Reusable skills | Present |

Vision lives in OCR-docs `docs/VISION.md` only.

---

## CCR Protocol

All production-grade decisions follow the CCR (Critical, Conservative, Recursive) protocol. See `OCR-docs/skills/ccr-protocol.knowledge.md` for full spec. Also available locally at `.ocr-standards/skills/` after propagation.

---

*Derived from OCR-docs/docs/VISION.md*
*Last updated: April 5 2026*
*Owner: Matt*
*Status: ACTIVE*
