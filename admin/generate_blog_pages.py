#!/usr/bin/env python3
"""
Generate Individual Blog Post HTML Pages
Creates standalone HTML files for each blog post with full styling
"""

import json
import os
from pathlib import Path
from datetime import datetime

def generate_blog_page(post):
    """Generate a single blog post HTML page"""
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-84N5NNXLPX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-84N5NNXLPX', {{
            'send_page_view': true,
            'anonymize_ip': true
        }});
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post.get('title', 'Blog Post')} - Virginia Home Essentials</title>
    <meta name="description" content="{post.get('excerpt', 'Read our latest article')}">
    <meta name="keywords" content="Virginia, home, {post.get('category', 'home')}, {', '.join(post.get('tags', []))}">
    <link rel="stylesheet" href="../assets/styles.css">
    <link rel="stylesheet" href="blog-styles.css">
    <style>
        .blog-post-container {{
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .blog-header {{
            margin-bottom: 30px;
        }}
        .blog-meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        .blog-meta span {{
            margin-right: 20px;
        }}
        .blog-featured-image {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .blog-content {{
            line-height: 1.8;
            color: #333;
            font-size: 16px;
        }}
        .blog-content h2 {{
            margin-top: 30px;
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        .blog-content ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        .blog-content li {{
            margin-bottom: 10px;
        }}
        .blog-footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .back-to-blog {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }}
        .back-to-blog:hover {{
            background: #2980b9;
        }}
        @media (max-width: 768px) {{
            .blog-post-container {{
                margin: 20px 10px;
                padding: 15px;
            }}
            .blog-content {{
                font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="navbar">
            <div class="nav-container">
                <a href="../index.html" class="logo">Virginia Home Essentials</a>
                <ul class="nav-menu">
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="index.html">Blog</a></li>
                    <li><a href="../index.html#products">Products</a></li>
                    <li><a href="../index.html#about">About</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <div class="blog-post-container">
            <article>
                <div class="blog-header">
                    <h1>{post.get('title', 'Blog Post')}</h1>
                    <div class="blog-meta">
                        <span class="category-badge" style="background: #3498db; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px;">{post.get('category', 'General').replace('-', ' ').title()}</span>
                        <span>By {post.get('author', 'Virginia Home Essentials Team')}</span>
                        <span>Published: {post.get('publish_date', 'January 10, 2026')}</span>
                        <span>{post.get('read_time', '5 min read')} read</span>
                    </div>
                </div>

                {f'<img src="{post.get("featured_image")}" alt="{post.get("title")}" class="blog-featured-image">' if post.get('featured_image') else ''}

                <div class="blog-content">
                    {post.get('content', '<p>Content not available</p>')}
                </div>

                <div class="blog-footer">
                    <p><strong>Tags:</strong> {', '.join(post.get('tags', []))}</p>
                    <a href="index.html" class="back-to-blog">← Back to Blog</a>
                </div>
            </article>
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 Virginia Home Essentials. All rights reserved.</p>
        <p><a href="https://www.amazon.com" target="_blank">Amazon Affiliate</a></p>
    </footer>

    <script src="../assets/script.js"></script>
</body>
</html>'''
    
    return html_template


def create_sample_blog_posts():
    """Create sample blog posts with full content"""
    
    sample_posts = [
        {
            "id": 1,
            "title": "10 Essential Smart Home Devices for Virginia Homeowners",
            "slug": "smart-home-essentials-virginia",
            "category": "smart-home",
            "excerpt": "Transform your Virginia home with these must-have smart home devices that enhance security, comfort, and energy efficiency.",
            "author": "Virginia Home Essentials Team",
            "publish_date": "January 10, 2026",
            "read_time": "8 min read",
            "featured_image": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "tags": ["smart-home", "technology", "energy-efficient"],
            "content": """
<p>Moving to a new home in Virginia? Smart home technology can make your transition easier and your daily life more convenient. In this guide, we'll explore the top 10 smart home devices that every Virginia homeowner should consider.</p>

<h2>1. Smart Thermostats</h2>
<p>Smart thermostats like Nest and Ecobee are essential for Virginia's variable climate. They learn your schedule and adjust temperature automatically, saving you up to 15% on heating and cooling costs.</p>

<h2>2. Smart Lighting Systems</h2>
<p>Control your home's lighting from anywhere with smart bulbs and switches. Philips Hue and LIFX offer color options and scheduling that can enhance your home's ambiance.</p>

<h2>3. Smart Security Cameras</h2>
<p>Ring and Arlo cameras provide peace of mind with 24/7 monitoring, motion detection, and cloud storage. Perfect for watching your property while you're away.</p>

<h2>4. Smart Door Locks</h2>
<p>Never worry about forgetting your keys again. Smart locks let you unlock your door remotely and track who comes and goes.</p>

<h2>5. Smart Speakers</h2>
<p>Amazon Echo and Google Home serve as central hubs for your smart home while offering entertainment, information, and voice control.</p>

<h2>6. Smart Plugs</h2>
<p>Convert regular appliances into smart devices with smart plugs. Monitor energy usage and control devices remotely.</p>

<h2>7. Smart Water Leak Detectors</h2>
<p>Protect your Virginia home from water damage with leak detectors that alert you immediately to problems.</p>

<h2>8. Smart Garage Door Openers</h2>
<p>Control and monitor your garage door from your phone, adding convenience and security.</p>

<h2>9. Smart Sprinkler Controllers</h2>
<p>Rachio and Hunter smart controllers optimize your irrigation based on weather, saving water and money.</p>

<h2>10. Smart Refrigerators</h2>
<p>Modern smart fridges help manage groceries, recipes, and family schedules efficiently.</p>

<h2>Getting Started</h2>
<p>Start with a smart hub like Amazon Echo or Google Home, then gradually add devices. Most integrate seamlessly and improve your quality of life significantly.</p>
            """
        },
        {
            "id": 2,
            "title": "Virginia Real Estate Market Update: January 2026",
            "slug": "virginia-market-update-january-2026",
            "category": "market-insights",
            "excerpt": "Latest Virginia housing market trends, price analysis, and insights for homebuyers and sellers.",
            "author": "Market Analysis Team",
            "publish_date": "January 9, 2026",
            "read_time": "6 min read",
            "featured_image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "tags": ["market-insights", "real-estate", "virginia"],
            "content": """
<p>The Virginia real estate market continues to show positive momentum heading into 2026. Here's what you need to know about current conditions and trends.</p>

<h2>Market Overview</h2>
<p>Virginia's housing market remains relatively stable with modest price appreciation and healthy inventory levels. Average home prices continue to reflect regional variations.</p>

<h2>Northern Virginia Market</h2>
<p>Northern Virginia, especially Fairfax County and Arlington, continues to attract buyers with strong job markets and good schools. Median prices remain higher but inventory has improved.</p>

<h2>Richmond Market</h2>
<p>Richmond's market offers better affordability while still being close to urban amenities. New development projects continue to drive growth in desired neighborhoods.</p>

<h2>Buyer Tips for 2026</h2>
<ul>
<li>Get pre-approved before house hunting</li>
<li>Consider first-time buyer programs available in Virginia</li>
<li>Factor in Virginia's low property tax rates</li>
<li>Explore expanding neighborhoods for better value</li>
</ul>

<h2>Seller Insights</h2>
<p>If you're considering selling, January and February can be good months for homes in good condition. Competition from other sellers is typically lower than spring.</p>

<h2>Looking Ahead</h2>
<p>As we move into spring, expect increased activity and competition. The best time to buy is often when you're ready - the right property at the right price makes the best investment.</p>
            """
        },
        {
            "id": 3,
            "title": "Best Kitchen Essentials for New Virginia Homeowners",
            "slug": "kitchen-essentials-new-homeowners",
            "category": "product-guides",
            "excerpt": "Create your dream kitchen with these essential appliances and tools for new homeowners.",
            "author": "Product Team",
            "publish_date": "January 8, 2026",
            "read_time": "7 min read",
            "featured_image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "tags": ["kitchen", "appliances", "home-setup"],
            "content": """
<p>A well-equipped kitchen is essential for any new homeowner. Whether you're starting from scratch or upgrading, here are the must-have items for a functional Virginia kitchen.</p>

<h2>Essential Appliances</h2>
<p>Every kitchen needs the basics: a reliable refrigerator, stove, oven, and dishwasher. Consider energy-efficient models to save on utility costs.</p>

<h2>Small Appliances</h2>
<ul>
<li><strong>Coffee Maker:</strong> Start your day right with a quality coffee machine</li>
<li><strong>Microwave:</strong> Essential for quick meals and reheating</li>
<li><strong>Toaster:</strong> Better than your oven for toast</li>
<li><strong>Blender:</strong> Great for smoothies and food prep</li>
<li><strong>Food Processor:</strong> Saves time on meal preparation</li>
</ul>

<h2>Cookware and Bakeware</h2>
<p>Invest in quality pots, pans, and baking sheets. Non-stick cookware makes cooking easier, while stainless steel lasts longer.</p>

<h2>Kitchen Tools</h2>
<p>Don't forget the essentials: knives, cutting boards, utensils, measuring cups, and mixing bowls. Quality tools make cooking more enjoyable.</p>

<h2>Organization Solutions</h2>
<p>Keep your kitchen organized with storage containers, drawer organizers, and shelving units. A tidy kitchen is a functional kitchen.</p>

<h2>Lighting and Aesthetics</h2>
<p>Proper lighting improves functionality and safety. Add some decorative touches to make your kitchen feel like home.</p>

<h2>Budget Tips</h2>
<p>You don't need to buy everything at once. Start with essentials and add items as your needs and budget allow.</p>
            """
        },
        {
            "id": 4,
            "title": "Winter Home Maintenance Checklist for Virginia",
            "slug": "winter-maintenance-virginia",
            "category": "home-maintenance",
            "excerpt": "Prepare your Virginia home for winter with this comprehensive maintenance checklist.",
            "author": "Maintenance Experts",
            "publish_date": "January 7, 2026",
            "read_time": "9 min read",
            "featured_image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "tags": ["maintenance", "winter", "home-care"],
            "content": """
<p>Virginia winters can be unpredictable. Ensure your home is prepared with this essential maintenance checklist.</p>

<h2>HVAC System</h2>
<ul>
<li>Schedule professional HVAC inspection</li>
<li>Replace furnace filters regularly</li>
<li>Check thermostat batteries</li>
<li>Clean vents and ducts</li>
</ul>

<h2>Roof and Gutters</h2>
<p>Clear gutters of leaves and debris to prevent ice dams. Inspect roof for missing shingles or damage.</p>

<h2>Windows and Doors</h2>
<p>Seal any gaps around windows and doors to prevent drafts. Check weatherstripping and caulking.</p>

<h2>Plumbing Protection</h2>
<ul>
<li>Drain exterior hoses and faucets</li>
<li>Insulate exposed pipes</li>
<li>Know where your water shut-off valve is located</li>
<li>Fix any leaks promptly</li>
</ul>

<h2>Exterior Preparation</h2>
<p>Trim tree branches that could fall on your house. Check for cracks in foundation or siding.</p>

<h2>Interior Preparations</h2>
<ul>
<li>Test your heating system in advance</li>
<li>Ensure you have snow removal equipment</li>
<li>Stock up on supplies for potential power outages</li>
<li>Test carbon monoxide detectors</li>
</ul>

<h2>Emergency Preparedness</h2>
<p>Keep emergency supplies on hand including blankets, flashlights, and first aid kits.</p>

<h2>Professional Help</h2>
<p>Don't hesitate to call professionals for inspections and repairs. Preventive maintenance saves money in the long run.</p>
            """
        }
    ]
    
    return sample_posts


def main():
    """Generate blog post HTML pages"""
    
    # Get sample posts
    posts = create_sample_blog_posts()
    
    # Get blog directory
    blog_dir = Path(__file__).parent.parent / "blog"
    blog_dir.mkdir(exist_ok=True)
    
    # Also create posts.json
    posts_json_path = blog_dir / "posts.json"
    
    # Prepare posts for JSON (without full content)
    json_posts = []
    for post in posts:
        json_post = {k: v for k, v in post.items() if k != 'content'}
        json_posts.append(json_post)
    
    # Save posts.json
    with open(posts_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_posts, f, indent=2, ensure_ascii=False)
    print(f"✅ Created {posts_json_path}")
    
    # Create individual blog post pages
    for post in posts:
        slug = post['slug']
        filename = blog_dir / f"{slug}.html"
        
        html_content = generate_blog_page(post)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Created {filename.name}")
    
    print(f"\n✅ Successfully generated {len(posts)} blog post pages!")
    print(f"✅ Posts JSON file: {posts_json_path}")
    

if __name__ == "__main__":
    main()
