# SKILL.md — OurSharedMagnets (OSM)

Skills for working in the OurSharedMagnets repo.

---

## Skill: Postman Collection Build

### When to Use
User says: "postman", "collection", "api docs", "newman"

### Steps
1. Read OCR-docs `docs/VISION.md` for product registry
2. Read OSE `CLAUDE.md` for API contract and route table
3. Build Postman collection mirroring all OSE endpoints
4. Organize by: public routes, admin routes, form routes, feature flag routes
5. Include environment variables for staging and production
6. Add Newman CI scripts for automated API testing
7. Document in `collections/`

---

## Skill: Franchise Playbook

### When to Use
User says: "franchise", "playbook", "corridor playbook", "operator guide"

### Steps
1. Read OCR-docs `docs/VISION.md` for product registry and corridor definitions
2. Compile operational knowledge from all products:
   - OSG: game night format and setup
   - OSP: onboarding and recognition
   - OSR: archive capture process
   - OW: music integration
   - OSE: platform usage
3. Structure as step-by-step runbook for a new corridor operator
4. Document in `docs/playbook/`

---

## Skill: API Documentation

### When to Use
User says: "api docs", "document api", "developer guide"

### Steps
1. Read OSE `CLAUDE.md` for route table and API contract
2. Document each endpoint: method, path, auth, request/response, examples
3. Include error responses and edge cases
4. Map feature flag behavior per tier (Free/Mid/Enterprise)
5. Document in `docs/api/`

---

## Skill: Ritual Execution Skill File

### When to Use
User says: "ritual skill", "execution skill", "how to run"

### Steps
1. Read OCR-docs `docs/VISION.md` for product roles
2. Define the ritual execution sequence: pre-event setup → event execution → post-event capture
3. Map which product handles each step
4. Create a single-file skill that a corridor operator can follow end-to-end
5. Document in `docs/skills/`

---

*Last updated: April 5 2026*
*Owner: Matt*
*Status: ACTIVE*
