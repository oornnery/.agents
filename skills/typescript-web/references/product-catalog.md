# Product Catalog

Use to choose a sellable package and prevent scope explosion.

## Starter Presence

For first website/presence.

MVP: home, services/products, about/trust, gallery, testimonials/review highlights, contact, WhatsApp CTA, address/map, local SEO metadata.

Avoid: login/admin, CMS unless client will update content, backend for static content.

## Landing Conversion

For one offer, campaign, treatment, event, or launch.

MVP: hero promise, problem, offer, proof, FAQ, lead form, WhatsApp CTA, success/thank-you state.

Optional: CRM/Zapier/Make webhook, later A/B copy, analytics events.

## Booking System

For appointments: clinics, dentists, salons, barbers, beauty, services by schedule.

MVP: service catalog, professional/resource selection, slots, booking form, confirmation, admin list/calendar, status `pending|confirmed|canceled`, notification/webhook.

Entities: services, professionals/resources, availability_rules, appointments, customers.

Guardrail: no medical records unless explicitly scoped.

## Ordering System

For restaurant, pizzeria, snack bar, delivery, service orders.

MVP: categories, products/options/add-ons, cart, customer/contact, pickup/delivery, order summary, WhatsApp/admin queue, admin status.

Entities: categories, products, product_options, orders, order_items, customers.

Guardrail: payment integration is phase 2 unless requested.

## Catalog Commerce

For market, store, distributor, light commerce.

MVP: categories, search/filter, product detail, cart/order intent, WhatsApp/admin checkout, admin catalog CRUD, optional stock visibility.

Entities: categories, products, optional inventory_movements, orders, order_items.

Guardrail: avoid full marketplace/ecommerce complexity by default.

## Admin Dashboard

For internal ops, cash-flow, leads, lightweight CRM.

MVP: CRUD entries, categories/statuses, date filters, summary cards, CSV export, optional roles.

Entities by domain. Cash-flow usually needs categories, transactions, optional accounts/daily_closings.

Guardrail: cash-flow is operational, not accounting software.
