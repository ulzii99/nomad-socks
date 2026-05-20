/**
 * API client for Nomad Socks backend
 * Handles all communication with the Django REST API.
 */

const API_BASE = 'http://localhost:8001/api/v1';

const api = {
    async get(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return response.json();
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return response.json();
    },

    /** Fetch all products, optionally filtered */
    async getProducts(params = {}) {
        const qs = new URLSearchParams(params).toString();
        const url = qs ? `/products/?${qs}` : '/products/';
        const data = await this.get(url);
        return data.results || data;
    },

    /** Fetch featured products */
    async getFeaturedProducts() {
        return this.get('/products/featured/');
    },

    /** Fetch a single product by slug */
    async getProductBySlug(slug) {
        return this.get(`/products/${slug}/`);
    },

    /** Fetch a single product by ID (finds slug first from cache) */
    async getProductById(id) {
        // Use cached products to find slug, then fetch detail
        if (_productCache.length > 0) {
            const cached = _productCache.find(p => p.id === parseInt(id));
            if (cached) {
                return this.getProductBySlug(cached.slug);
            }
        }
        // Fallback: fetch all and find
        const products = await this.getProducts();
        const product = products.find(p => p.id === parseInt(id));
        if (product) {
            return this.getProductBySlug(product.slug);
        }
        return null;
    },

    /** Fetch related products for a given product slug */
    async getRelatedProducts(slug) {
        return this.get(`/products/${slug}/related/`);
    },

    /** Fetch all categories */
    async getCategories() {
        const data = await this.get('/categories/');
        return data.results || data;
    },

    /** Submit contact form */
    async submitContact(data) {
        return this.post('/contact/', data);
    },

    /** Subscribe to newsletter */
    async subscribeNewsletter(email) {
        return this.post('/newsletter/subscribe/', { email });
    },

    // --- Auth ---

    /** Register a new user */
    async register(data) {
        return this.post('/accounts/register/', data);
    },

    /** Login and get tokens */
    async login(username, password) {
        const tokens = await this.post('/accounts/token/', { username, password });
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
        return tokens;
    },

    /** Logout (clear tokens) */
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    /** Get stored access token */
    getToken() {
        return localStorage.getItem('access_token');
    },

    /** Check if user is logged in */
    isAuthenticated() {
        return !!this.getToken();
    },

    /** Make an authenticated GET request */
    async authGet(endpoint) {
        const token = this.getToken();
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`${API_BASE}${endpoint}`, { headers });
        if (response.status === 401) {
            // Try to refresh
            const refreshed = await this.refreshToken();
            if (refreshed) return this.authGet(endpoint);
            throw new Error('Authentication required');
        }
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return response.json();
    },

    /** Make an authenticated POST request */
    async authPost(endpoint, data) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        };
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers,
            body: JSON.stringify(data),
        });
        if (response.status === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) return this.authPost(endpoint, data);
            throw new Error('Authentication required');
        }
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return response.json();
    },

    /** Make an authenticated PATCH request */
    async authPatch(endpoint, data) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        };
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify(data),
        });
        if (response.status === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) return this.authPatch(endpoint, data);
            throw new Error('Authentication required');
        }
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return response.json();
    },

    /** Make an authenticated DELETE request */
    async authDelete(endpoint) {
        const token = this.getToken();
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE',
            headers,
        });
        if (response.status === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) return this.authDelete(endpoint);
            throw new Error('Authentication required');
        }
        if (!response.ok && response.status !== 204) throw new Error(`API error: ${response.status}`);
        return response.status === 204 ? null : response.json();
    },

    /** Refresh the access token */
    async refreshToken() {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) return false;
        try {
            const response = await fetch(`${API_BASE}/accounts/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh }),
            });
            if (!response.ok) {
                this.logout();
                return false;
            }
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } catch {
            this.logout();
            return false;
        }
    },

    /** Get current user profile */
    async getProfile() {
        return this.authGet('/accounts/profile/');
    },

    // --- Cart ---

    async getCart() {
        return this.authGet('/cart/');
    },

    async addToCart(productId, size, quantity) {
        return this.authPost('/cart/items/', { product_id: productId, size, quantity });
    },

    async updateCartItem(itemId, quantity) {
        return this.authPatch(`/cart/items/${itemId}/`, { quantity });
    },

    async removeCartItem(itemId) {
        return this.authDelete(`/cart/items/${itemId}/`);
    },

    async clearCart() {
        return this.authDelete('/cart/clear/');
    },

    // --- Orders ---

    async checkout(data) {
        return this.authPost('/orders/checkout/', data);
    },

    async getOrders() {
        return this.authGet('/orders/');
    },

    async getOrder(orderNumber) {
        return this.authGet(`/orders/${orderNumber}/`);
    },
};

// Product cache — loaded once, used to map IDs to slugs and provide sync access
let _productCache = [];
let _productCachePromise = null;

/**
 * Load all products into cache. Called once on page load.
 * Returns the cached products array.
 */
async function loadProductCache() {
    if (_productCachePromise) return _productCachePromise;
    _productCachePromise = api.getProducts().then(products => {
        _productCache = products;
        return products;
    });
    return _productCachePromise;
}

/**
 * Get a product from cache by ID (synchronous, for cart display).
 * Returns null if cache not loaded or product not found.
 */
function getCachedProductById(id) {
    return _productCache.find(p => p.id === parseInt(id)) || null;
}
