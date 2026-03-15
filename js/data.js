/**
 * Product Data for Nomad Socks
 * This file contains all product information.
 * In the future, this will be replaced with API calls to a backend.
 */

const PRODUCTS = [
    {
        id: 1,
        name: "Classic Black Everyday Socks",
        price: 8.99,
        category: "classic",
        description: "Timeless black cotton socks perfect for everyday wear. Soft, breathable, and durable.",
        features: [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable"
        ],
        featured: true
    },
    {
        id: 2,
        name: "Classic White Everyday Socks",
        price: 8.99,
        category: "classic",
        description: "Clean white cotton socks for a fresh, classic look. Great for work or casual wear.",
        features: [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable"
        ],
        featured: true
    },
    {
        id: 3,
        name: "Classic Gray Everyday Socks",
        price: 8.99,
        category: "classic",
        description: "Versatile gray socks that go with everything. A wardrobe essential.",
        features: [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable"
        ],
        featured: false
    },
    {
        id: 4,
        name: "Classic Navy Everyday Socks",
        price: 8.99,
        category: "classic",
        description: "Deep navy blue socks perfect for professional settings or casual days.",
        features: [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable"
        ],
        featured: false
    },
    {
        id: 5,
        name: "Nomad Stripe Pattern Socks",
        price: 10.99,
        category: "patterned",
        description: "Bold stripes inspired by traditional Mongolian patterns. Stand out from the crowd.",
        features: [
            "Premium cotton blend with enhanced durability",
            "Unique nomadic stripe design",
            "Reinforced heel and toe",
            "Machine washable"
        ],
        featured: true
    },
    {
        id: 6,
        name: "Steppe Earth Tone Socks",
        price: 10.99,
        category: "patterned",
        description: "Warm earth tones inspired by the Mongolian steppe. Subtle pattern for everyday style.",
        features: [
            "Premium cotton blend with enhanced durability",
            "Earth-inspired color palette",
            "Reinforced heel and toe",
            "Machine washable"
        ],
        featured: true
    },
    {
        id: 7,
        name: "Geometric Pattern Socks",
        price: 10.99,
        category: "patterned",
        description: "Modern geometric patterns meet traditional inspiration. Perfect for adding personality.",
        features: [
            "Premium cotton blend with enhanced durability",
            "Contemporary geometric design",
            "Reinforced heel and toe",
            "Machine washable"
        ],
        featured: false
    },
    {
        id: 8,
        name: "Desert Sunset Socks",
        price: 10.99,
        category: "patterned",
        description: "Gradient colors inspired by Gobi Desert sunsets. A beautiful everyday statement.",
        features: [
            "Premium cotton blend with enhanced durability",
            "Sunset-inspired gradient design",
            "Reinforced heel and toe",
            "Machine washable"
        ],
        featured: false
    },
    {
        id: 9,
        name: "Athletic Crew Socks",
        price: 9.99,
        category: "athletic",
        description: "Performance socks with extra cushioning for active days. Moisture-wicking and comfortable.",
        features: [
            "Moisture-wicking fabric blend",
            "Extra cushioning in sole",
            "Arch support",
            "Reinforced heel and toe"
        ],
        featured: false
    },
    {
        id: 10,
        name: "Low-Cut Athletic Socks",
        price: 8.49,
        category: "athletic",
        description: "Sleek low-cut design perfect for sneakers and athletic shoes. Stays hidden while keeping feet comfortable.",
        features: [
            "Low-cut design",
            "Moisture-wicking fabric blend",
            "Non-slip heel grip",
            "Lightweight and breathable"
        ],
        featured: false
    },
    {
        id: 11,
        name: "Classic Brown Everyday Socks",
        price: 8.99,
        category: "classic",
        description: "Rich brown cotton socks with a natural, earthy tone. Perfect for autumn and casual style.",
        features: [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable"
        ],
        featured: false
    },
    {
        id: 12,
        name: "Multi-Pack Classic Socks (5 pairs)",
        price: 34.99,
        category: "classic",
        description: "Value pack with 5 pairs of our classic everyday socks in assorted colors. Stock up and save!",
        features: [
            "5 pairs included (Black, White, Gray, Navy, Brown)",
            "Premium cotton blend",
            "Reinforced heel and toe",
            "Machine washable"
        ],
        featured: true
    }
];

/**
 * Get all products
 * @returns {Array} All products
 */
function getAllProducts() {
    return PRODUCTS;
}

/**
 * Get featured products
 * @returns {Array} Featured products
 */
function getFeaturedProducts() {
    return PRODUCTS.filter(p => p.featured);
}

/**
 * Get product by ID
 * @param {number} id - Product ID
 * @returns {Object|undefined} Product or undefined
 */
function getProductById(id) {
    return PRODUCTS.find(p => p.id === parseInt(id));
}

/**
 * Get products by category
 * @param {string} category - Category name
 * @returns {Array} Products in category
 */
function getProductsByCategory(category) {
    if (category === 'all') return PRODUCTS;
    return PRODUCTS.filter(p => p.category === category);
}

/**
 * Sort products
 * @param {Array} products - Products to sort
 * @param {string} sortBy - Sort method
 * @returns {Array} Sorted products
 */
function sortProducts(products, sortBy) {
    const sorted = [...products];
    switch (sortBy) {
        case 'price-low':
            return sorted.sort((a, b) => a.price - b.price);
        case 'price-high':
            return sorted.sort((a, b) => b.price - a.price);
        case 'name':
            return sorted.sort((a, b) => a.name.localeCompare(b.name));
        case 'featured':
        default:
            return sorted.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
    }
}

/**
 * Get related products (same category, excluding current product)
 * @param {number} productId - Current product ID
 * @param {number} limit - Max number of related products
 * @returns {Array} Related products
 */
function getRelatedProducts(productId, limit = 4) {
    const product = getProductById(productId);
    if (!product) return [];

    return PRODUCTS
        .filter(p => p.category === product.category && p.id !== productId)
        .slice(0, limit);
}
