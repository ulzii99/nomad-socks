/**
 * Product Data for Nomad Socks
 *
 * This file provides product data functions used across the site.
 * It tries to load data from the Django API first, falling back to
 * the static PRODUCTS array if the backend is unavailable.
 */

// Static fallback data — used when backend is unavailable
const STATIC_PRODUCTS = [
    {
        id: 1, name: "Classic Black Everyday Socks", name_en: "Classic Black Everyday Socks",
        name_mn: "Сонгодог хар өдөр тутмын оймс", price: 8.99, category: "classic",
        description: "Timeless black cotton socks perfect for everyday wear. Soft, breathable, and durable.",
        description_en: "Timeless black cotton socks perfect for everyday wear. Soft, breathable, and durable.",
        features: ["Premium cotton blend (80% cotton, 17% polyester, 3% elastane)", "Reinforced heel and toe", "Comfortable elastic band that stays up", "Machine washable"],
        featured: true, slug: "classic-black-everyday-socks"
    },
    {
        id: 2, name: "Classic White Everyday Socks", name_en: "Classic White Everyday Socks",
        name_mn: "Сонгодог цагаан өдөр тутмын оймс", price: 8.99, category: "classic",
        description: "Clean white cotton socks for a fresh, classic look. Great for work or casual wear.",
        description_en: "Clean white cotton socks for a fresh, classic look. Great for work or casual wear.",
        features: ["Premium cotton blend (80% cotton, 17% polyester, 3% elastane)", "Reinforced heel and toe", "Comfortable elastic band that stays up", "Machine washable"],
        featured: true, slug: "classic-white-everyday-socks"
    },
    {
        id: 3, name: "Classic Gray Everyday Socks", name_en: "Classic Gray Everyday Socks",
        name_mn: "Сонгодог саарал өдөр тутмын оймс", price: 8.99, category: "classic",
        description: "Versatile gray socks that go with everything. A wardrobe essential.",
        description_en: "Versatile gray socks that go with everything. A wardrobe essential.",
        features: ["Premium cotton blend (80% cotton, 17% polyester, 3% elastane)", "Reinforced heel and toe", "Comfortable elastic band that stays up", "Machine washable"],
        featured: false, slug: "classic-gray-everyday-socks"
    },
    {
        id: 4, name: "Classic Navy Everyday Socks", name_en: "Classic Navy Everyday Socks",
        name_mn: "Сонгодог хар хөх өдөр тутмын оймс", price: 8.99, category: "classic",
        description: "Deep navy blue socks perfect for professional settings or casual days.",
        description_en: "Deep navy blue socks perfect for professional settings or casual days.",
        features: ["Premium cotton blend (80% cotton, 17% polyester, 3% elastane)", "Reinforced heel and toe", "Comfortable elastic band that stays up", "Machine washable"],
        featured: false, slug: "classic-navy-everyday-socks"
    },
    {
        id: 5, name: "Nomad Stripe Pattern Socks", name_en: "Nomad Stripe Pattern Socks",
        name_mn: "Номад судалт хээтэй оймс", price: 10.99, category: "patterned",
        description: "Bold stripes inspired by traditional Mongolian patterns. Stand out from the crowd.",
        description_en: "Bold stripes inspired by traditional Mongolian patterns. Stand out from the crowd.",
        features: ["Premium cotton blend with enhanced durability", "Unique nomadic stripe design", "Reinforced heel and toe", "Machine washable"],
        featured: true, slug: "nomad-stripe-pattern-socks"
    },
    {
        id: 6, name: "Steppe Earth Tone Socks", name_en: "Steppe Earth Tone Socks",
        name_mn: "Тал нутгийн газрын өнгөт оймс", price: 10.99, category: "patterned",
        description: "Warm earth tones inspired by the Mongolian steppe. Subtle pattern for everyday style.",
        description_en: "Warm earth tones inspired by the Mongolian steppe. Subtle pattern for everyday style.",
        features: ["Premium cotton blend with enhanced durability", "Earth-inspired color palette", "Reinforced heel and toe", "Machine washable"],
        featured: true, slug: "steppe-earth-tone-socks"
    },
    {
        id: 7, name: "Geometric Pattern Socks", name_en: "Geometric Pattern Socks",
        name_mn: "Геометр хээтэй оймс", price: 10.99, category: "patterned",
        description: "Modern geometric patterns meet traditional inspiration. Perfect for adding personality.",
        description_en: "Modern geometric patterns meet traditional inspiration. Perfect for adding personality.",
        features: ["Premium cotton blend with enhanced durability", "Contemporary geometric design", "Reinforced heel and toe", "Machine washable"],
        featured: false, slug: "geometric-pattern-socks"
    },
    {
        id: 8, name: "Desert Sunset Socks", name_en: "Desert Sunset Socks",
        name_mn: "Говийн нарны жаргалт оймс", price: 10.99, category: "patterned",
        description: "Gradient colors inspired by Gobi Desert sunsets. A beautiful everyday statement.",
        description_en: "Gradient colors inspired by Gobi Desert sunsets. A beautiful everyday statement.",
        features: ["Premium cotton blend with enhanced durability", "Sunset-inspired gradient design", "Reinforced heel and toe", "Machine washable"],
        featured: false, slug: "desert-sunset-socks"
    },
    {
        id: 9, name: "Athletic Crew Socks", name_en: "Athletic Crew Socks",
        name_mn: "Спорт crew оймс", price: 9.99, category: "athletic",
        description: "Performance socks with extra cushioning for active days. Moisture-wicking and comfortable.",
        description_en: "Performance socks with extra cushioning for active days. Moisture-wicking and comfortable.",
        features: ["Moisture-wicking fabric blend", "Extra cushioning in sole", "Arch support", "Reinforced heel and toe"],
        featured: false, slug: "athletic-crew-socks"
    },
    {
        id: 10, name: "Low-Cut Athletic Socks", name_en: "Low-Cut Athletic Socks",
        name_mn: "Богино спорт оймс", price: 8.49, category: "athletic",
        description: "Sleek low-cut design perfect for sneakers and athletic shoes. Stays hidden while keeping feet comfortable.",
        description_en: "Sleek low-cut design perfect for sneakers and athletic shoes. Stays hidden while keeping feet comfortable.",
        features: ["Low-cut design", "Moisture-wicking fabric blend", "Non-slip heel grip", "Lightweight and breathable"],
        featured: false, slug: "low-cut-athletic-socks"
    },
    {
        id: 11, name: "Classic Brown Everyday Socks", name_en: "Classic Brown Everyday Socks",
        name_mn: "Сонгодог хүрэн өдөр тутмын оймс", price: 8.99, category: "classic",
        description: "Rich brown cotton socks with a natural, earthy tone. Perfect for autumn and casual style.",
        description_en: "Rich brown cotton socks with a natural, earthy tone. Perfect for autumn and casual style.",
        features: ["Premium cotton blend (80% cotton, 17% polyester, 3% elastane)", "Reinforced heel and toe", "Comfortable elastic band that stays up", "Machine washable"],
        featured: false, slug: "classic-brown-everyday-socks"
    },
    {
        id: 12, name: "Multi-Pack Classic Socks (5 pairs)", name_en: "Multi-Pack Classic Socks (5 pairs)",
        name_mn: "Олон багц сонгодог оймс (5 хос)", price: 34.99, category: "classic",
        description: "Value pack with 5 pairs of our classic everyday socks in assorted colors. Stock up and save!",
        description_en: "Value pack with 5 pairs of our classic everyday socks in assorted colors. Stock up and save!",
        features: ["5 pairs included (Black, White, Gray, Navy, Brown)", "Premium cotton blend", "Reinforced heel and toe", "Machine washable"],
        featured: true, slug: "multi-pack-classic-socks-5-pairs"
    }
];

// Active product list — starts with static data, replaced by API data when available
let PRODUCTS = [...STATIC_PRODUCTS];

// Track whether we're using the API
let _usingApi = false;

/**
 * Normalize API product to match the format the frontend expects.
 * The API returns name_en/name_mn, but the frontend also uses .name and .description.
 */
function normalizeProduct(p) {
    return {
        ...p,
        name: p.name_en || p.name,
        description: p.description_en || p.description,
        price: parseFloat(p.price),
        // If API returns features as objects, extract text
        features: Array.isArray(p.features)
            ? p.features.map(f => typeof f === 'object' ? f.text_en : f)
            : p.features,
    };
}

/**
 * Initialize product data from the API.
 * Falls back silently to static data if the backend is unavailable.
 */
async function initProductData() {
    try {
        const apiProducts = await api.getProducts();
        if (apiProducts && apiProducts.length > 0) {
            PRODUCTS = apiProducts.map(normalizeProduct);
            _usingApi = true;
            console.log(`Loaded ${PRODUCTS.length} products from API`);
        }
    } catch (err) {
        console.warn('Backend unavailable, using static product data:', err.message);
    }
}

function getAllProducts() {
    return PRODUCTS;
}

function getFeaturedProducts() {
    return PRODUCTS.filter(p => p.featured);
}

function getProductById(id) {
    return PRODUCTS.find(p => p.id === parseInt(id));
}

function getProductsByCategory(category) {
    if (category === 'all') return PRODUCTS;
    return PRODUCTS.filter(p => p.category === category);
}

function sortProducts(products, sortBy) {
    const sorted = [...products];
    switch (sortBy) {
        case 'price-low':
            return sorted.sort((a, b) => a.price - b.price);
        case 'price-high':
            return sorted.sort((a, b) => b.price - a.price);
        case 'name':
            return sorted.sort((a, b) => (a.name_en || a.name).localeCompare(b.name_en || b.name));
        case 'featured':
        default:
            return sorted.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
    }
}

function getRelatedProducts(productId, limit = 4) {
    const product = getProductById(productId);
    if (!product) return [];
    return PRODUCTS
        .filter(p => p.category === product.category && p.id !== productId)
        .slice(0, limit);
}
