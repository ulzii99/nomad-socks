/**
 * Cart functionality for Nomad Socks
 * Uses localStorage to persist cart data.
 * Ready for backend integration in the future.
 */

const CART_STORAGE_KEY = 'nomad_socks_cart';

/**
 * Cart object with all cart-related methods
 */
const Cart = {
    /**
     * Get cart items from localStorage
     * @returns {Array} Cart items
     */
    getItems() {
        const cartData = localStorage.getItem(CART_STORAGE_KEY);
        return cartData ? JSON.parse(cartData) : [];
    },

    /**
     * Save cart items to localStorage
     * @param {Array} items - Cart items to save
     */
    saveItems(items) {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
        this.updateCartCount();
    },

    /**
     * Add item to cart
     * @param {number} productId - Product ID
     * @param {string} size - Size selected
     * @param {number} quantity - Quantity to add
     * @returns {boolean} Success status
     */
    addItem(productId, size, quantity = 1) {
        const product = getProductById(productId);
        if (!product) return false;

        const items = this.getItems();
        const existingIndex = items.findIndex(
            item => item.productId === productId && item.size === size
        );

        if (existingIndex >= 0) {
            items[existingIndex].quantity += quantity;
        } else {
            items.push({
                productId,
                size,
                quantity,
                addedAt: new Date().toISOString()
            });
        }

        this.saveItems(items);
        return true;
    },

    /**
     * Update item quantity
     * @param {number} productId - Product ID
     * @param {string} size - Size
     * @param {number} quantity - New quantity
     */
    updateQuantity(productId, size, quantity) {
        const items = this.getItems();
        const index = items.findIndex(
            item => item.productId === productId && item.size === size
        );

        if (index >= 0) {
            if (quantity <= 0) {
                items.splice(index, 1);
            } else {
                items[index].quantity = quantity;
            }
            this.saveItems(items);
        }
    },

    /**
     * Remove item from cart
     * @param {number} productId - Product ID
     * @param {string} size - Size
     */
    removeItem(productId, size) {
        const items = this.getItems();
        const filtered = items.filter(
            item => !(item.productId === productId && item.size === size)
        );
        this.saveItems(filtered);
    },

    /**
     * Clear all items from cart
     */
    clear() {
        localStorage.removeItem(CART_STORAGE_KEY);
        this.updateCartCount();
    },

    /**
     * Get total number of items in cart
     * @returns {number} Total quantity
     */
    getTotalItems() {
        const items = this.getItems();
        return items.reduce((total, item) => total + item.quantity, 0);
    },

    /**
     * Get cart subtotal
     * @returns {number} Subtotal
     */
    getSubtotal() {
        const items = this.getItems();
        return items.reduce((total, item) => {
            const product = getProductById(item.productId);
            return total + (product ? product.price * item.quantity : 0);
        }, 0);
    },

    /**
     * Get cart with full product details
     * @returns {Array} Cart items with product details
     */
    getItemsWithDetails() {
        const items = this.getItems();
        return items.map(item => {
            const product = getProductById(item.productId);
            return {
                ...item,
                product
            };
        }).filter(item => item.product);
    },

    /**
     * Update cart count in header
     */
    updateCartCount() {
        const countElements = document.querySelectorAll('#cart-count');
        const count = this.getTotalItems();
        countElements.forEach(el => {
            el.textContent = count;
        });
    }
};

/**
 * Show a toast notification
 * @param {string} message - Message to show
 * @param {string} type - Type: 'success', 'error', or default
 */
function showToast(message, type = '') {
    // Remove existing toasts
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Format price for display
 * @param {number} price - Price value
 * @returns {string} Formatted price
 */
function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}
