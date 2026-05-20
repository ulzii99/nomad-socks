# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Nomad Socks** - Full-stack e-commerce website for a Mongolian sock business.

- **Business**: Family-owned sock manufacturing with 4 machines in Mongolia
- **Target**: Both local Mongolian and international customers
- **Products**: Casual everyday socks (12 products, 3 categories)

## Tech Stack

- **Frontend**: Plain HTML5, CSS3, JavaScript (no frameworks)
- **Backend**: Django 4.2 + Django REST Framework
- **Auth**: JWT via djangorestframework-simplejwt
- **Database**: SQLite (dev), PostgreSQL (production)
- **Payments**: QPay, SocialPay (MNT domestic), Stripe (USD international)
- **i18n**: Bilingual Mongolian/English via translations.js + DB fields

## Project Structure

```
sock_website/
├── index.html              # Homepage
├── products.html           # Product listing with filters
├── product.html            # Product detail (?id= param)
├── cart.html               # Shopping cart
├── checkout.html           # Checkout with shipping + payment
├── login.html              # Login
├── register.html           # Registration
├── account.html            # User account & order history
├── admin-dashboard.html    # Admin analytics dashboard
├── about.html              # About the business
├── contact.html            # Contact form
├── css/styles.css          # All styles
├── js/
│   ├── api.js              # API client (auth, cart, orders, payments)
│   ├── data.js             # Product data (API with static fallback)
│   ├── cart.js             # Cart logic (localStorage)
│   ├── translations.js     # Bilingual MN/EN translations
│   └── main.js             # Page init and UI interactions
└── backend/                # Django project
    ├── manage.py
    ├── requirements.txt
    ├── nomadsocks/          # Project config (settings, urls)
    ├── accounts/            # Custom User, JWT auth, profile
    ├── products/            # Product catalog, categories
    ├── cart/                # Server-side cart (session/user)
    ├── orders/              # Orders, checkout, status tracking
    ├── payments/            # QPay, SocialPay, Stripe providers
    ├── shipping/            # Zones, rates, shipments
    ├── inventory/           # Stock tracking, machines, production
    ├── content/             # Contact form, newsletter
    └── analytics/           # Dashboard, revenue reports
```

## Development

```bash
# Start backend (port 8001)
cd backend && python manage.py runserver 8001

# Start frontend (port 8000)
python -m http.server 8000

# Admin panel
http://localhost:8001/admin/  (admin / admin123)

# Admin dashboard
http://localhost:8000/admin-dashboard.html
```

## Backend Apps

| App | Purpose | Key Models |
|-----|---------|------------|
| accounts | Auth, profiles | Custom User |
| products | Catalog | Product, Category, ProductSize, ProductFeature |
| cart | Shopping cart | Cart, CartItem |
| orders | Checkout & tracking | Order, OrderItem, OrderStatusHistory |
| payments | Payment processing | Payment (QPay/SocialPay/Stripe providers) |
| shipping | Delivery | ShippingZone, ShippingRate, Shipment |
| inventory | Stock management | InventoryRecord, Machine, ProductionRun |
| content | Forms | ContactSubmission, NewsletterSubscriber |
| analytics | Reports | (queries other models, no own models) |

## API Endpoints

- `GET /api/v1/products/` — product list (filterable)
- `GET /api/v1/products/{slug}/` — product detail
- `GET /api/v1/categories/` — categories
- `POST /api/v1/accounts/register/` — register
- `POST /api/v1/accounts/token/` — JWT login
- `GET/POST /api/v1/cart/` — cart operations
- `POST /api/v1/orders/checkout/` — place order
- `POST /api/v1/payments/create/` — create payment
- `GET /api/v1/shipping/rates/` — shipping rates
- `POST /api/v1/contact/` — contact form
- `GET /api/v1/admin/dashboard/` — admin metrics
- `GET /api/v1/admin/inventory/` — stock overview

## Payment Integration

Payment providers are in `backend/payments/providers.py`. Each implements `create_invoice()` and `check_payment()`. Without API credentials, they return mock responses for development.

**To go live, set in settings.py:**
- `QPAY_USERNAME`, `QPAY_PASSWORD`, `QPAY_INVOICE_CODE`
- `SOCIALPAY_APP_ID`, `SOCIALPAY_SECRET`
- `STRIPE_SECRET_KEY`

## Frontend Architecture

- `js/api.js` — central API client with JWT auth (auto-refresh), all endpoints
- `js/data.js` — fetches products from API on load, falls back to static `STATIC_PRODUCTS`
- `js/main.js` — page routing, async init, auth UI updates
- Bilingual: products have `name_en`/`name_mn` from DB; UI strings via `translations.js`
- CSS variables in `:root`, responsive at 992px/768px/480px
