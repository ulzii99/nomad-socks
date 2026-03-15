/**
 * Main JavaScript for Nomad Socks
 * Handles page-specific functionality and UI interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Apply translations first
    applyTranslations();

    // Initialize cart count on all pages
    Cart.updateCartCount();

    // Mobile menu toggle
    initMobileMenu();

    // Initialize page content
    initPageContent();

    // Newsletter form (present on multiple pages)
    initNewsletterForm();
});

/**
 * Initialize page-specific content
 */
function initPageContent() {
    const path = window.location.pathname;

    if (path.endsWith('index.html') || path.endsWith('/') || path === '') {
        initHomePage();
    } else if (path.endsWith('products.html')) {
        initProductsPage();
    } else if (path.endsWith('product.html')) {
        initProductDetailPage();
    } else if (path.endsWith('cart.html')) {
        initCartPage();
    } else if (path.endsWith('contact.html')) {
        initContactPage();
    }
}

/**
 * Re-render page content when language changes
 * Called from translations.js toggleLanguage()
 */
function renderPageContent() {
    const path = window.location.pathname;

    if (path.endsWith('index.html') || path.endsWith('/') || path === '') {
        const featuredGrid = document.getElementById('featured-products');
        if (featuredGrid) {
            const featured = getFeaturedProducts();
            featuredGrid.innerHTML = featured.map(createProductCard).join('');
            attachAddToCartListeners(featuredGrid);
        }
    } else if (path.endsWith('products.html')) {
        const productsGrid = document.getElementById('products-grid');
        if (productsGrid) {
            const categoryFilter = document.getElementById('category-filter');
            const sortFilter = document.getElementById('sort-filter');
            const category = categoryFilter ? categoryFilter.value : 'all';
            const sortBy = sortFilter ? sortFilter.value : 'featured';

            let products = getProductsByCategory(category);
            products = sortProducts(products, sortBy);

            productsGrid.innerHTML = products.map(createProductCard).join('');
            attachAddToCartListeners(productsGrid);
        }
    } else if (path.endsWith('product.html')) {
        // Re-render related products
        const relatedGrid = document.getElementById('related-products');
        const urlParams = new URLSearchParams(window.location.search);
        const productId = urlParams.get('id');
        if (relatedGrid && productId) {
            const related = getRelatedProducts(parseInt(productId), 4);
            if (related.length > 0) {
                relatedGrid.innerHTML = related.map(createProductCard).join('');
            } else {
                const otherProducts = getAllProducts()
                    .filter(p => p.id !== parseInt(productId))
                    .slice(0, 4);
                relatedGrid.innerHTML = otherProducts.map(createProductCard).join('');
            }
            attachAddToCartListeners(relatedGrid);
        }
    } else if (path.endsWith('cart.html')) {
        renderCart();
    }
}

/**
 * Initialize mobile menu functionality
 */
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav') && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    }
}

/**
 * Get translated product name
 * @param {Object} product - Product data
 * @returns {string} Translated product name
 */
function getProductName(product) {
    const lang = getCurrentLang();
    if (lang === 'en') {
        return product.name;
    }

    // Map product IDs to translation keys
    const nameKeys = {
        1: 'product.classic.black',
        2: 'product.classic.white',
        3: 'product.classic.gray',
        4: 'product.classic.navy',
        5: 'product.nomad.stripe',
        6: 'product.steppe',
        7: 'product.geometric',
        8: 'product.desert.sunset',
        9: 'product.athletic.crew',
        10: 'product.athletic.lowcut',
        11: 'product.classic.brown',
        12: 'product.multipack'
    };

    const key = nameKeys[product.id];
    return key ? t(key) : product.name;
}

/**
 * Create product card HTML
 * @param {Object} product - Product data
 * @returns {string} HTML string
 */
function createProductCard(product) {
    const productName = getProductName(product);
    const addToCartText = t('products.addToCart');

    return `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-card-image">
                <a href="product.html?id=${product.id}">
                    <div class="placeholder-image" data-text="${productName.split(' ').slice(0, 2).join(' ')}"></div>
                </a>
            </div>
            <div class="product-card-body">
                <h3><a href="product.html?id=${product.id}">${productName}</a></h3>
                <p class="product-card-price">${formatPrice(product.price)}</p>
                <button class="btn btn-primary add-to-cart-btn"
                        data-product-id="${product.id}">
                    ${addToCartText}
                </button>
            </div>
        </div>
    `;
}

/**
 * Initialize home page
 */
function initHomePage() {
    const featuredGrid = document.getElementById('featured-products');
    if (featuredGrid) {
        const featured = getFeaturedProducts();
        featuredGrid.innerHTML = featured.map(createProductCard).join('');
        attachAddToCartListeners(featuredGrid);
    }
}

/**
 * Initialize products page
 */
function initProductsPage() {
    const productsGrid = document.getElementById('products-grid');
    const categoryFilter = document.getElementById('category-filter');
    const sortFilter = document.getElementById('sort-filter');

    if (!productsGrid) return;

    function renderProducts() {
        const category = categoryFilter ? categoryFilter.value : 'all';
        const sortBy = sortFilter ? sortFilter.value : 'featured';

        let products = getProductsByCategory(category);
        products = sortProducts(products, sortBy);

        productsGrid.innerHTML = products.map(createProductCard).join('');
        attachAddToCartListeners(productsGrid);
    }

    // Initial render
    renderProducts();

    // Filter change listeners
    if (categoryFilter) {
        categoryFilter.addEventListener('change', renderProducts);
    }
    if (sortFilter) {
        sortFilter.addEventListener('change', renderProducts);
    }
}

/**
 * Initialize product detail page
 */
function initProductDetailPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (!productId) {
        window.location.href = 'products.html';
        return;
    }

    const product = getProductById(productId);

    if (!product) {
        window.location.href = 'products.html';
        return;
    }

    const productName = getProductName(product);

    // Update page content
    document.title = `${productName} - Nomad Socks`;
    document.getElementById('product-breadcrumb').textContent = productName;
    document.getElementById('product-name').textContent = productName;
    document.getElementById('product-price').textContent = formatPrice(product.price);
    document.getElementById('product-description').textContent = product.description;

    // Update image placeholder
    const imageEl = document.querySelector('#product-image');
    if (imageEl) {
        imageEl.setAttribute('data-text', productName.split(' ').slice(0, 2).join(' '));
    }

    // Update features
    const featuresEl = document.getElementById('product-features');
    if (featuresEl && product.features) {
        featuresEl.innerHTML = product.features.map(f => `<li>${f}</li>`).join('');
    }

    // Quantity selector
    const qtyInput = document.getElementById('quantity-input');
    const qtyMinus = document.getElementById('qty-minus');
    const qtyPlus = document.getElementById('qty-plus');

    if (qtyMinus && qtyPlus && qtyInput) {
        qtyMinus.addEventListener('click', () => {
            const current = parseInt(qtyInput.value);
            if (current > 1) qtyInput.value = current - 1;
        });

        qtyPlus.addEventListener('click', () => {
            const current = parseInt(qtyInput.value);
            if (current < 10) qtyInput.value = current + 1;
        });

        qtyInput.addEventListener('change', () => {
            let value = parseInt(qtyInput.value);
            if (isNaN(value) || value < 1) value = 1;
            if (value > 10) value = 10;
            qtyInput.value = value;
        });
    }

    // Add to cart button
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', () => {
            const size = document.getElementById('size-select').value;
            const quantity = parseInt(qtyInput.value);

            if (Cart.addItem(product.id, size, quantity)) {
                const msg = `${quantity} ${productName} ${t('toast.addedToCart')}`;
                showToast(msg, 'success');
            }
        });
    }

    // Related products
    const relatedGrid = document.getElementById('related-products');
    if (relatedGrid) {
        const related = getRelatedProducts(product.id, 4);
        if (related.length > 0) {
            relatedGrid.innerHTML = related.map(createProductCard).join('');
            attachAddToCartListeners(relatedGrid);
        } else {
            // Show other products if no related in same category
            const otherProducts = getAllProducts()
                .filter(p => p.id !== product.id)
                .slice(0, 4);
            relatedGrid.innerHTML = otherProducts.map(createProductCard).join('');
            attachAddToCartListeners(relatedGrid);
        }
    }
}

/**
 * Initialize cart page
 */
function initCartPage() {
    renderCart();
}

/**
 * Render cart items and summary
 */
function renderCart() {
    const cartItemsEl = document.getElementById('cart-items');
    const cartEmptyEl = document.getElementById('cart-empty');
    const cartSummaryEl = document.getElementById('cart-summary');
    const subtotalEl = document.getElementById('cart-subtotal');
    const totalEl = document.getElementById('cart-total');

    if (!cartItemsEl) return;

    const items = Cart.getItemsWithDetails();

    if (items.length === 0) {
        cartItemsEl.style.display = 'none';
        cartSummaryEl.style.display = 'none';
        cartEmptyEl.style.display = 'block';
        return;
    }

    cartItemsEl.style.display = 'block';
    cartSummaryEl.style.display = 'block';
    cartEmptyEl.style.display = 'none';

    const eachText = t('cart.each');
    const removeText = t('cart.remove');

    // Render cart items
    cartItemsEl.innerHTML = items.map(item => {
        const productName = getProductName(item.product);
        return `
            <div class="cart-item" data-product-id="${item.productId}" data-size="${item.size}">
                <div class="cart-item-image">
                    <a href="product.html?id=${item.productId}">
                        <div class="placeholder-image" data-text="${productName.split(' ').slice(0, 2).join(' ')}"></div>
                    </a>
                </div>
                <div class="cart-item-details">
                    <h3><a href="product.html?id=${item.productId}">${productName}</a></h3>
                    <p class="cart-item-meta">${t('product.size')} ${item.size}</p>
                    <p class="cart-item-price">${formatPrice(item.product.price)} ${eachText}</p>
                    <div class="quantity-selector">
                        <button type="button" class="qty-btn cart-qty-minus">−</button>
                        <input type="number" class="cart-qty-input" value="${item.quantity}" min="1" max="10">
                        <button type="button" class="qty-btn cart-qty-plus">+</button>
                    </div>
                </div>
                <div class="cart-item-actions">
                    <span class="cart-item-total">${formatPrice(item.product.price * item.quantity)}</span>
                    <button class="remove-btn">${removeText}</button>
                </div>
            </div>
        `;
    }).join('');

    // Update summary
    const subtotal = Cart.getSubtotal();
    subtotalEl.textContent = formatPrice(subtotal);
    totalEl.textContent = formatPrice(subtotal);

    // Attach event listeners to cart items
    attachCartItemListeners();
}

/**
 * Attach event listeners to cart item controls
 */
function attachCartItemListeners() {
    const cartItems = document.querySelectorAll('.cart-item');

    cartItems.forEach(item => {
        const productId = parseInt(item.dataset.productId);
        const size = item.dataset.size;

        const minusBtn = item.querySelector('.cart-qty-minus');
        const plusBtn = item.querySelector('.cart-qty-plus');
        const qtyInput = item.querySelector('.cart-qty-input');
        const removeBtn = item.querySelector('.remove-btn');

        minusBtn.addEventListener('click', () => {
            const current = parseInt(qtyInput.value);
            if (current > 1) {
                Cart.updateQuantity(productId, size, current - 1);
                renderCart();
            }
        });

        plusBtn.addEventListener('click', () => {
            const current = parseInt(qtyInput.value);
            if (current < 10) {
                Cart.updateQuantity(productId, size, current + 1);
                renderCart();
            }
        });

        qtyInput.addEventListener('change', () => {
            let value = parseInt(qtyInput.value);
            if (isNaN(value) || value < 1) value = 1;
            if (value > 10) value = 10;
            Cart.updateQuantity(productId, size, value);
            renderCart();
        });

        removeBtn.addEventListener('click', () => {
            Cart.removeItem(productId, size);
            showToast(t('toast.removedFromCart'));
            renderCart();
        });
    });

    // Checkout button
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            showToast(t('toast.checkoutSoon'), 'success');
        });
    }
}

/**
 * Attach add to cart listeners to product cards
 * @param {HTMLElement} container - Container with product cards
 */
function attachAddToCartListeners(container) {
    const buttons = container.querySelectorAll('.add-to-cart-btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = parseInt(btn.dataset.productId);
            const product = getProductById(productId);

            if (product && Cart.addItem(productId, 'M', 1)) {
                const productName = getProductName(product);
                const msg = `${productName} ${t('toast.addedToCart')}`;
                showToast(msg, 'success');
            }
        });
    });
}

/**
 * Initialize newsletter form
 */
function initNewsletterForm() {
    const form = document.getElementById('newsletter-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            showToast(t('toast.subscribed'), 'success');
            form.reset();
        });
    }
}

/**
 * Initialize contact page
 */
function initContactPage() {
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            showToast(t('toast.messageSent'), 'success');
            form.reset();
        });
    }
}
