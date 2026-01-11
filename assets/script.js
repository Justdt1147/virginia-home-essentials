// Virginia Home Essentials - Main JavaScript

// Product Data with Amazon Affiliate Integration
const productData = {
    'smart-home': [
        {
            id: 1,
            title: "Amazon Echo Dot (5th Gen)",
            description: "Smart speaker with Alexa - perfect for new homeowners to control lights, music, and more",
            price: "$49.99",
            rating: 4.6,
            reviews: "125,432",
            image: "https://images.unsplash.com/photo-1543512214-318c7553f230?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B09B8V1LZ3", // Replace with actual affiliate link
            category: "smart-home",
            trending: true
        },
        {
            id: 2,
            title: "Philips Hue White Smart Bulbs",
            description: "4-pack smart LED bulbs that work with Alexa, Google Assistant, and Apple HomeKit",
            price: "$59.99",
            rating: 4.5,
            reviews: "89,234",
            image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07354SP1C",
            category: "smart-home"
        },
        {
            id: 3,
            title: "Ring Video Doorbell",
            description: "1080p HD video doorbell with motion detection and two-way talk",
            price: "$99.99",
            rating: 4.4,
            reviews: "156,789",
            image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B08N5NQ869",
            category: "smart-home"
        },
        {
            id: 4,
            title: "Nest Learning Thermostat",
            description: "Smart thermostat that learns your schedule and saves energy automatically",
            price: "$249.99",
            rating: 4.3,
            reviews: "67,543",
            image: "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa0?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B0131RG6VK",
            category: "smart-home"
        }
    ],
    'security': [
        {
            id: 5,
            title: "SimpliSafe Home Security System",
            description: "Complete wireless home security system with 24/7 monitoring",
            price: "$199.99",
            rating: 4.6,
            reviews: "45,678",
            image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07YDVJZ4Q",
            category: "security",
            trending: true
        },
        {
            id: 6,
            title: "Arlo Essential Indoor Camera",
            description: "1080p wireless security camera with night vision and two-way audio",
            price: "$79.99",
            rating: 4.2,
            reviews: "23,456",
            image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B08HRNG8CR",
            category: "security"
        },
        {
            id: 7,
            title: "August Smart Lock Pro",
            description: "Smart lock with WiFi connectivity - control access from anywhere",
            price: "$279.99",
            rating: 4.1,
            reviews: "34,567",
            image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B0752V8D8D",
            category: "security"
        }
    ],
    'kitchen': [
        {
            id: 8,
            title: "Instant Pot Duo 7-in-1",
            description: "Electric pressure cooker, slow cooker, rice cooker, and more in one",
            price: "$79.95",
            rating: 4.7,
            reviews: "234,567",
            image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B00FLYWNYQ",
            category: "kitchen",
            trending: true
        },
        {
            id: 9,
            title: "Ninja Foodi Personal Blender",
            description: "Compact blender perfect for smoothies and single servings",
            price: "$39.99",
            rating: 4.5,
            reviews: "78,901",
            image: "https://images.unsplash.com/photo-1570197788417-0e82375c9371?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07GBZ1Y3H",
            category: "kitchen"
        },
        {
            id: 10,
            title: "Cuisinart Air Fryer Toaster Oven",
            description: "Compact countertop oven with air frying capability",
            price: "$199.99",
            rating: 4.4,
            reviews: "56,789",
            image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B077HBQZPX",
            category: "kitchen"
        }
    ],
    'tools': [
        {
            id: 11,
            title: "BLACK+DECKER 20V MAX Drill",
            description: "Cordless drill/driver with LED light - essential for new homeowners",
            price: "$49.99",
            rating: 4.3,
            reviews: "45,678",
            image: "https://images.unsplash.com/photo-1504148455328-c376907d081c?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B00AQZGKZ6",
            category: "tools",
            trending: true
        },
        {
            id: 12,
            title: "Stanley 25ft Tape Measure",
            description: "Heavy-duty measuring tape with standout blade",
            price: "$12.99",
            rating: 4.6,
            reviews: "89,012",
            image: "https://images.unsplash.com/photo-1504148455328-c376907d081c?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B00002X204",
            category: "tools"
        },
        {
            id: 13,
            title: "CRAFTSMAN Home Tool Kit",
            description: "230-piece mechanics tool set with hard case",
            price: "$149.99",
            rating: 4.5,
            reviews: "23,456",
            image: "https://images.unsplash.com/photo-1504148455328-c376907d081c?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07QK7TGBX",
            category: "tools"
        }
    ],
    'decor': [
        {
            id: 14,
            title: "SONGMICS Floating Shelves",
            description: "Set of 3 rustic wood floating shelves for wall decor",
            price: "$29.99",
            rating: 4.4,
            reviews: "34,567",
            image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07DLCQZPX",
            category: "decor"
        },
        {
            id: 15,
            title: "Bedsure Throw Pillows Set",
            description: "4-pack decorative throw pillows for couch and bed",
            price: "$24.99",
            rating: 4.3,
            reviews: "67,890",
            image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
            amazonUrl: "https://amazon.com/dp/B07VQZQZPX",
            category: "decor",
            trending: true
        }
    ]
};

// Blog Data
const blogData = [
    {
        id: 1,
        title: "10 Smart Home Essentials Every New Virginia Homeowner Needs",
        excerpt: "Transform your new home into a smart home with these must-have devices that enhance security, comfort, and energy efficiency.",
        image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        date: "December 8, 2025",
        category: "Smart Home",
        readTime: "5 min read",
        url: "blog/smart-home-essentials.html"
    },
    {
        id: 2,
        title: "Virginia Housing Market Update: What New Buyers Need to Know",
        excerpt: "Latest trends in Virginia's real estate market, including inventory increases and what it means for first-time buyers.",
        image: "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        date: "December 7, 2025",
        category: "Market Insights",
        readTime: "7 min read",
        url: "blog/virginia-market-update.html"
    },
    {
        id: 3,
        title: "First-Time Home Buyer's Kitchen Setup Guide",
        excerpt: "Essential kitchen appliances and tools that every new homeowner should have, from basic cookware to smart appliances.",
        image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        date: "December 6, 2025",
        category: "Kitchen",
        readTime: "6 min read",
        url: "blog/kitchen-setup-guide.html"
    }
];

// DOM Elements
const productsContainer = document.getElementById('products-container');
const blogContainer = document.getElementById('blog-container');
const categoryTabs = document.querySelectorAll('.tab-btn');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadProducts('smart-home');
    loadBlogPosts();
    setupEventListeners();
    setupSmoothScrolling();
    setupNewsletterForm();
});

// Product Functions
function loadProducts(category) {
    if (!productsContainer) return;
    
    productsContainer.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    
    setTimeout(() => {
        const products = productData[category] || [];
        productsContainer.innerHTML = '';
        
        products.forEach(product => {
            const productCard = createProductCard(product);
            productsContainer.appendChild(productCard);
        });
    }, 500);
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const trendingBadge = product.trending ? '<span class="trending-badge">🔥 Trending</span>' : '';
    
    card.innerHTML = `
        <div class="product-image">
            <img src="${product.image}" alt="${product.title}" loading="lazy">
            ${trendingBadge}
        </div>
        <div class="product-info">
            <h3 class="product-title">${product.title}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-price">${product.price}</div>
            <div class="product-rating">
                <div class="stars">${generateStars(product.rating)}</div>
                <span class="rating-text">${product.rating} (${product.reviews} reviews)</span>
            </div>
            <button class="product-btn" onclick="trackAndRedirect('${product.amazonUrl}', '${product.title}', '${product.category}')">
                View on Amazon
            </button>
        </div>
    `;
    
    return card;
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '★';
    }
    
    if (hasHalfStar) {
        stars += '☆';
    }
    
    return stars;
}

// Blog Functions
function loadBlogPosts() {
    if (!blogContainer) return;
    
    blogContainer.innerHTML = '';
    
    blogData.slice(0, 3).forEach(post => {
        const blogCard = createBlogCard(post);
        blogContainer.appendChild(blogCard);
    });
}

function createBlogCard(post) {
    const card = document.createElement('div');
    card.className = 'blog-card';
    
    card.innerHTML = `
        <div class="blog-image">
            <img src="${post.image}" alt="${post.title}" loading="lazy">
        </div>
        <div class="blog-content">
            <div class="blog-meta">
                <span><i class="fas fa-calendar"></i> ${post.date}</span>
                <span><i class="fas fa-tag"></i> ${post.category}</span>
                <span><i class="fas fa-clock"></i> ${post.readTime}</span>
            </div>
            <h3 class="blog-title">${post.title}</h3>
            <p class="blog-excerpt">${post.excerpt}</p>
            <a href="${post.url}" class="btn-primary">Read More</a>
        </div>
    `;
    
    return card;
}

// Event Listeners
function setupEventListeners() {
    // Category tabs
    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active tab
            categoryTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Load products for category
            loadProducts(category);
            
            // Track category selection
            trackEvent('category_selected', {
                category: category,
                timestamp: new Date().toISOString()
            });
        });
    });
    
    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }
}

// Smooth Scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Newsletter Form
function setupNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            // Here you would typically send the email to your backend
            // For now, we'll just show a success message
            alert('Thank you for subscribing! You\'ll receive our weekly newsletter with the latest Virginia real estate insights and home essentials.');
            
            // Track newsletter signup
            trackEvent('newsletter_signup', {
                email: email,
                timestamp: new Date().toISOString()
            });
            
            this.reset();
        });
    }
}

// Analytics and Tracking
function trackAndRedirect(amazonUrl, productTitle, category) {
    // Track product click with Google Analytics (if available)
    if (typeof gtag !== 'undefined') {
        gtag('event', 'affiliate_click', {
            'event_category': 'Product',
            'event_label': productTitle,
            'product_category': category,
            'value': 1
        });
    }
    
    // Track product click locally
    trackEvent('product_click', {
        product: productTitle,
        category: category,
        url: amazonUrl,
        timestamp: new Date().toISOString()
    });
    
    // Add affiliate tracking parameters if needed
    const affiliateUrl = addAffiliateParams(amazonUrl);
    
    // Open in new tab
    window.open(affiliateUrl, '_blank');
}

function addAffiliateParams(url) {
    // Add your Amazon Associate tag here
    const associateTag = 'virginiahomee-20'; // Replace with your actual tag
    
    if (url.includes('amazon.com')) {
        const separator = url.includes('?') ? '&' : '?';
        return `${url}${separator}tag=${associateTag}`;
    }
    
    return url;
}

function trackEvent(eventName, eventData) {
    // Send to Google Analytics if available
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    }
    
    // Store events in localStorage for backup
    const events = JSON.parse(localStorage.getItem('site_events') || '[]');
    events.push({
        event: eventName,
        data: eventData
    });
    localStorage.setItem('site_events', JSON.stringify(events));
    
    console.log('Event tracked:', eventName, eventData);
}

// AI Content Generation Functions (for admin use)
function generateProductRecommendations(userPreferences) {
    // This would integrate with AI services to generate personalized recommendations
    const recommendations = [];
    
    Object.keys(productData).forEach(category => {
        if (userPreferences.categories.includes(category)) {
            const categoryProducts = productData[category];
            const topProducts = categoryProducts
                .filter(p => p.rating >= userPreferences.minRating)
                .sort((a, b) => b.rating - a.rating)
                .slice(0, userPreferences.maxPerCategory || 2);
            
            recommendations.push(...topProducts);
        }
    });
    
    return recommendations;
}

function generateBlogContent(topic, keywords) {
    // This would integrate with AI content generation services
    // For now, return a template structure
    return {
        title: `${topic}: A Complete Guide for Virginia Homeowners`,
        outline: [
            'Introduction',
            'Key Considerations',
            'Product Recommendations',
            'Virginia-Specific Tips',
            'Conclusion and Next Steps'
        ],
        keywords: keywords,
        estimatedLength: '1500-2000 words',
        targetAudience: 'New homeowners in Virginia'
    };
}

// Market Data Integration
async function fetchMarketData() {
    // This would integrate with real estate APIs
    // For now, return mock data based on our research
    return {
        inventory: {
            current: 36801,
            change: '+18.0%',
            period: 'Year over year'
        },
        medianPrice: {
            nova: '$1,250,000',
            statewide: '$425,000',
            change: '+5.2%'
        },
        trends: [
            'Buyer\'s market emerging in Northern Virginia',
            'Inventory levels increasing across the state',
            'First-time buyer programs expanding'
        ]
    };
}

// Utility Functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Export functions for admin panel use
window.VirginiaHomeEssentials = {
    generateProductRecommendations,
    generateBlogContent,
    fetchMarketData,
    trackEvent,
    productData,
    blogData
};

// Add CSS for trending badge
const style = document.createElement('style');
style.textContent = `
    .product-image {
        position: relative;
    }
    
    .trending-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #ff4444;
        color: white;
        padding: 0;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        z-index: 1;
    }
`;
document.head.appendChild(style);

