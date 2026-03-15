# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Nomad Socks** - E-commerce website for a Mongolian sock business. Currently a static frontend with plans for backend integration.

- **Business**: Family-owned sock manufacturing with 4 machines in Mongolia
- **Target**: Both local Mongolian and international customers
- **Products**: Casual everyday socks

## Tech Stack

- Plain HTML5, CSS3, JavaScript (no frameworks)
- LocalStorage for cart persistence
- Designed for future backend integration

## Project Structure

```
sock_website/
├── index.html          # Homepage with hero, features, featured products
├── products.html       # Product listing with filters
├── product.html        # Single product detail (uses ?id= query param)
├── cart.html           # Shopping cart
├── about.html          # About the business
├── contact.html        # Contact form
├── css/
│   └── styles.css      # All styles, CSS variables at top
└── js/
    ├── data.js         # Product data and helper functions
    ├── cart.js         # Cart logic (localStorage-based)
    └── main.js         # Page initialization and UI interactions
```

## Development

Open `index.html` directly in browser, or use any local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve
```

## Architecture Notes

### Product Data (`js/data.js`)
- `PRODUCTS` array contains all product objects
- Helper functions: `getAllProducts()`, `getFeaturedProducts()`, `getProductById()`, `getProductsByCategory()`, `sortProducts()`
- **Backend migration**: Replace these functions with API calls

### Cart System (`js/cart.js`)
- `Cart` object with methods: `getItems()`, `addItem()`, `updateQuantity()`, `removeItem()`, `clear()`
- Uses localStorage key `nomad_socks_cart`
- `showToast()` for user feedback
- **Backend migration**: Replace localStorage with API calls, keep same interface

### Page Routing (`js/main.js`)
- Detects current page via `window.location.pathname`
- Product detail page uses `?id=` query parameter
- Each page has its own init function: `initHomePage()`, `initProductsPage()`, etc.

### CSS Theming
- Color palette inspired by Mongolian landscape (earth tones, sky blues)
- CSS variables defined in `:root` for easy theming
- Responsive breakpoints: 992px, 768px, 480px

## Placeholder Images

Images use CSS-generated placeholders via `.placeholder-image` class with `data-text` attribute. Replace with actual `<img>` tags when images are available.

## Future Backend Integration Points

1. **Product data**: Replace `js/data.js` functions with fetch calls
2. **Cart**: Replace localStorage in `Cart` object with API calls
3. **Forms**: Newsletter and contact forms currently show toast only - add actual submission
4. **Checkout**: Button currently shows "coming soon" toast
5. **User accounts**: No auth system yet - add when backend ready
