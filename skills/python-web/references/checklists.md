# Checklists

## Planning

- [ ] Business/product brief created
- [ ] Facts, assumptions, unknowns separated
- [ ] Profile/package selected
- [ ] MVP, phase 2, out of scope defined
- [ ] Route map, template map, flows, data model defined
- [ ] Auth/admin/DB/migration/deployment decisions recorded
- [ ] Acceptance criteria written

## Website/Landing

- [ ] Responsive hero + clear CTA
- [ ] Services/products visible
- [ ] Contact/WhatsApp/address/map/hours present when relevant
- [ ] Trust signals and FAQ when useful
- [ ] SEO title/description and Open Graph metadata
- [ ] Accessible headings/buttons
- [ ] Mobile layout verified

## Booking

- [ ] Services/resources/availability modeled
- [ ] Booking form validates input
- [ ] Confirmation state works
- [ ] Admin sees appointments and changes status
- [ ] No sensitive health records by default

## Ordering/Catalog

- [ ] Categories/products modeled
- [ ] Cart/order flow works
- [ ] Customer contact captured minimally
- [ ] WhatsApp/admin handoff works
- [ ] Admin product/order updates work if scoped

## Admin/Cash-Flow

- [ ] Entries/categories/statuses work
- [ ] Date filters and summaries are accurate
- [ ] CSV export works if scoped
- [ ] Scope is not pretending to be full accounting

## Quality

- [ ] `uv run ruff format --check .` passes
- [ ] `uv run ruff check .` passes
- [ ] `uv run ty check` passes
- [ ] `uv run pytest` passes
- [ ] Alembic upgrade works if DB is used
- [ ] Empty/loading/error states exist
- [ ] Server-side validation exists
- [ ] Admin routes protected
- [ ] Secrets are not committed
- [ ] README/docs updated

## Final Response

Mention files changed, behavior added, validation commands, assumptions, and remaining questions/next steps.
