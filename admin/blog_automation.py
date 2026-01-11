#!/usr/bin/env python3
"""
Virginia Home Essentials - Blog Automation System
Automated blog post generation, scheduling, and publishing
"""

import json
import datetime
import os
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
import requests
from pathlib import Path
import markdown
import schedule
import time

# SQLite timeout configuration for concurrent access
DEFAULT_SQLITE_TIMEOUT = 30  # seconds

@dataclass
class BlogPost:
    id: str
    title: str
    slug: str
    content: str
    excerpt: str
    category: str
    tags: List[str]
    author: str
    publish_date: str
    status: str  # draft, scheduled, published
    seo_title: str
    meta_description: str
    featured_image: str
    read_time: str
    affiliate_products: List[str]

@dataclass
class ContentIdea:
    topic: str
    category: str
    keywords: List[str]
    seasonal_relevance: str
    priority_score: float
    target_audience: str
    content_type: str  # guide, review, comparison, news

class BlogAutomationSystem:
    def __init__(self, openai_api_key: str = None):
        """Initialize the blog automation system"""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.db_path = "blog_system.db"
        self.blog_dir = "../blog"
        self.init_database()
        self.init_blog_directory()
        
        # Virginia-specific content themes
        self.content_themes = {
            "seasonal": {
                "winter": ["heating efficiency", "winter prep", "holiday decor", "energy savings"],
                "spring": ["spring cleaning", "garden prep", "home maintenance", "allergy solutions"],
                "summer": ["cooling solutions", "outdoor living", "energy efficiency", "vacation prep"],
                "fall": ["fall maintenance", "winterization", "holiday prep", "cozy decor"]
            },
            "market_insights": [
                "Virginia housing market trends", "first-time buyer programs", 
                "interest rate impacts", "regional market analysis", "investment opportunities"
            ],
            "product_categories": [
                "smart home essentials", "security systems", "kitchen appliances",
                "home tools", "decor ideas", "energy efficiency"
            ],
            "homeowner_guides": [
                "first-time buyer checklist", "home maintenance schedule",
                "DIY vs professional", "budget planning", "insurance tips"
            ]
        }
        
        # SEO keywords for Virginia market
        self.seo_keywords = {
            "primary": ["Virginia homes", "new homeowners", "Virginia real estate", "home essentials"],
            "location": ["Northern Virginia", "Richmond", "Virginia Beach", "Norfolk", "Alexandria"],
            "product": ["smart home", "home security", "kitchen appliances", "home tools"],
            "intent": ["buying guide", "reviews", "comparison", "tips", "checklist"]
        }

    def init_database(self):
        """Initialize SQLite database for blog management"""
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
        cursor = conn.cursor()
        
        # Blog posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                category TEXT,
                tags TEXT,
                author TEXT,
                publish_date TEXT,
                status TEXT,
                seo_title TEXT,
                meta_description TEXT,
                featured_image TEXT,
                read_time TEXT,
                affiliate_products TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Content ideas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                category TEXT,
                keywords TEXT,
                seasonal_relevance TEXT,
                priority_score REAL,
                target_audience TEXT,
                content_type TEXT,
                status TEXT,
                created_at TEXT
            )
        ''')
        
        # Publishing schedule table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publishing_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT,
                scheduled_date TEXT,
                status TEXT,
                FOREIGN KEY (post_id) REFERENCES blog_posts (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def init_blog_directory(self):
        """Initialize blog directory structure"""
        Path(self.blog_dir).mkdir(exist_ok=True)
        Path(f"{self.blog_dir}/posts").mkdir(exist_ok=True)
        Path(f"{self.blog_dir}/images").mkdir(exist_ok=True)
        Path(f"{self.blog_dir}/drafts").mkdir(exist_ok=True)

    def generate_content_ideas(self, count: int = 20) -> List[ContentIdea]:
        """Generate content ideas based on trends and seasonality"""
        
        current_month = datetime.datetime.now().month
        current_season = self._get_current_season(current_month)
        
        ideas = []
        
        # Seasonal content ideas
        seasonal_topics = self.content_themes["seasonal"][current_season]
        for topic in seasonal_topics:
            idea = ContentIdea(
                topic=f"{topic.title()} Guide for Virginia Homeowners",
                category="seasonal",
                keywords=[topic, "Virginia", "homeowners", current_season],
                seasonal_relevance=current_season,
                priority_score=0.8,
                target_audience="New homeowners",
                content_type="guide"
            )
            ideas.append(idea)
        
        # Market insights
        for topic in self.content_themes["market_insights"]:
            idea = ContentIdea(
                topic=f"{topic.title()}: December 2025 Update",
                category="market-insights",
                keywords=topic.split() + ["2025", "Virginia"],
                seasonal_relevance="year-round",
                priority_score=0.9,
                target_audience="Prospective buyers",
                content_type="news"
            )
            ideas.append(idea)
        
        # Product guides
        for category in self.content_themes["product_categories"]:
            idea = ContentIdea(
                topic=f"Best {category.title()} for New Virginia Homeowners",
                category="product-guide",
                keywords=category.split() + ["Virginia", "new homeowners", "buying guide"],
                seasonal_relevance="year-round",
                priority_score=0.7,
                target_audience="New homeowners",
                content_type="review"
            )
            ideas.append(idea)
        
        # Save ideas to database
        self._save_content_ideas(ideas)
        
        return ideas[:count]

    def _get_current_season(self, month: int) -> str:
        """Determine current season based on month"""
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"

    def _save_content_ideas(self, ideas: List[ContentIdea]):
        """Save content ideas to database"""
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        cursor = conn.cursor()
        
        for idea in ideas:
            cursor.execute('''
                INSERT OR IGNORE INTO content_ideas 
                (topic, category, keywords, seasonal_relevance, priority_score, 
                 target_audience, content_type, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                idea.topic, idea.category, json.dumps(idea.keywords),
                idea.seasonal_relevance, idea.priority_score, idea.target_audience,
                idea.content_type, "pending", datetime.datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()

    def generate_blog_post(self, content_idea: ContentIdea) -> BlogPost:
        """Generate a complete blog post from a content idea"""
        
        # Generate unique ID and slug
        post_id = self._generate_post_id()
        slug = self._generate_slug(content_idea.topic)
        
        # Generate content based on type
        if content_idea.content_type == "guide":
            content = self._generate_guide_content(content_idea)
        elif content_idea.content_type == "review":
            content = self._generate_review_content(content_idea)
        elif content_idea.content_type == "comparison":
            content = self._generate_comparison_content(content_idea)
        else:
            content = self._generate_general_content(content_idea)
        
        # Generate SEO elements
        seo_title = self._generate_seo_title(content_idea.topic)
        meta_description = self._generate_meta_description(content_idea)
        
        # Create blog post
        blog_post = BlogPost(
            id=post_id,
            title=content_idea.topic,
            slug=slug,
            content=content,
            excerpt=self._generate_excerpt(content),
            category=content_idea.category,
            tags=content_idea.keywords,
            author="Virginia Home Essentials Team",
            publish_date="",  # Will be set when scheduled
            status="draft",
            seo_title=seo_title,
            meta_description=meta_description,
            featured_image=self._get_featured_image(content_idea.category),
            read_time=self._calculate_read_time(content),
            affiliate_products=self._identify_affiliate_products(content_idea)
        )
        
        # Save to database
        self._save_blog_post(blog_post)
        
        return blog_post

    def _generate_guide_content(self, idea: ContentIdea) -> str:
        """Generate guide-style content"""
        
        template = f"""
# {idea.topic}

As a new homeowner in Virginia, you're embarking on an exciting journey. Whether you've just purchased your first home in Northern Virginia, Richmond, or Virginia Beach, this comprehensive guide will help you navigate {idea.topic.lower()}.

## Why This Matters for Virginia Homeowners

Virginia's unique climate and housing market present specific challenges and opportunities. With the current market showing increased inventory and buyer-friendly conditions, now is an excellent time to focus on making your new home comfortable and efficient.

## Essential Considerations

### 1. Virginia Climate Factors
Virginia's humid subtropical climate means you'll experience hot, humid summers and mild winters. This affects everything from your HVAC needs to seasonal maintenance requirements.

### 2. Regional Variations
- **Northern Virginia**: Higher costs but more amenities
- **Richmond Area**: Balanced market with good value
- **Coastal Areas**: Hurricane preparedness considerations
- **Rural Areas**: Well water and septic considerations

## Step-by-Step Guide

### Phase 1: Assessment and Planning
Before making any purchases or changes, assess your current situation:

1. **Evaluate Your Current Setup**
   - What's already installed or included?
   - What are your immediate needs vs. nice-to-haves?
   - What's your budget for improvements?

2. **Research Virginia-Specific Requirements**
   - Local building codes and regulations
   - HOA restrictions if applicable
   - Seasonal considerations

### Phase 2: Implementation
Based on your assessment, prioritize your actions:

1. **Immediate Needs** (First 30 days)
2. **Short-term Improvements** (First 6 months)
3. **Long-term Upgrades** (Year 1 and beyond)

### Phase 3: Maintenance and Optimization
Establish routines to maintain and improve your investments over time.

## Product Recommendations

Based on our research and Virginia homeowner feedback, here are our top recommendations:

### Essential Items
- [Product recommendations would be inserted here based on category]

### Budget-Friendly Options
- [Alternative recommendations for cost-conscious buyers]

### Premium Upgrades
- [High-end options for those with larger budgets]

## Virginia-Specific Tips

### Seasonal Considerations
- **Spring**: Focus on HVAC maintenance and outdoor prep
- **Summer**: Energy efficiency and cooling solutions
- **Fall**: Winterization and storm preparation
- **Winter**: Indoor comfort and energy conservation

### Local Resources
- Virginia Housing Development Authority (VHDA) programs
- Local utility rebates and incentives
- Regional contractors and service providers

## Common Mistakes to Avoid

1. **Rushing into major purchases** without proper research
2. **Ignoring seasonal factors** in your planning
3. **Overlooking local regulations** and requirements
4. **Not budgeting for maintenance** and ongoing costs

## Next Steps

Now that you have a comprehensive understanding of {idea.topic.lower()}, here's what to do next:

1. **Create Your Action Plan**: Prioritize based on your needs and budget
2. **Research Specific Products**: Use our affiliate links to find the best deals
3. **Connect with Local Professionals**: For installations and major work
4. **Join Our Community**: Subscribe to our newsletter for ongoing tips and updates

## Conclusion

{idea.topic} doesn't have to be overwhelming. By taking a systematic approach and leveraging Virginia-specific insights, you can make informed decisions that will serve you well for years to come.

Remember, every Virginia home is unique, and what works in Northern Virginia might need adjustment for the Richmond area or coastal regions. Take your time, do your research, and don't hesitate to consult with local professionals when needed.

---

*This guide is part of our comprehensive resource library for Virginia homeowners. For more tips, product recommendations, and market insights, explore our other articles and subscribe to our newsletter.*
        """
        
        return template.strip()

    def _generate_review_content(self, idea: ContentIdea) -> str:
        """Generate product review content"""
        
        template = f"""
# {idea.topic}

Finding the right products for your new Virginia home can be overwhelming. With countless options available, how do you choose what's truly worth your investment? We've done the research for you.

## Our Selection Criteria

When evaluating products for Virginia homeowners, we consider:

- **Climate Compatibility**: How well does it handle Virginia's humid summers and mild winters?
- **Value for Money**: Best bang for your buck, especially for first-time buyers
- **Reliability**: Products that will last through Virginia's weather variations
- **Local Availability**: Easy to find parts and service in Virginia
- **Energy Efficiency**: Important for managing utility costs

## Top Recommendations

### Best Overall: [Product Name]
**Price Range**: $XXX - $XXX
**Rating**: ⭐⭐⭐⭐⭐ (4.8/5)

**Why We Love It:**
- Excellent performance in Virginia's climate
- Great value for the price point
- Highly rated by local homeowners
- Energy efficient design

**Pros:**
- [Specific benefits]
- [Performance highlights]
- [User-friendly features]

**Cons:**
- [Minor limitations]
- [Considerations for some users]

**Best For**: New homeowners looking for reliable, all-around performance

### Best Budget Option: [Product Name]
**Price Range**: $XXX - $XXX
**Rating**: ⭐⭐⭐⭐ (4.3/5)

[Similar detailed review format]

### Premium Choice: [Product Name]
**Price Range**: $XXX - $XXX
**Rating**: ⭐⭐⭐⭐⭐ (4.9/5)

[Similar detailed review format]

## Comparison Table

| Feature | Budget Option | Best Overall | Premium Choice |
|---------|---------------|--------------|----------------|
| Price | $XXX | $XXX | $XXX |
| Warranty | X years | X years | X years |
| Energy Rating | X | X | X |
| Virginia Climate Rating | Good | Excellent | Excellent |

## Installation and Setup

### DIY vs Professional Installation
- **DIY Friendly**: [Products suitable for self-installation]
- **Professional Recommended**: [Products requiring expert installation]
- **Virginia Contractors**: Tips for finding qualified local installers

### First-Time Setup Tips
1. Read all documentation before starting
2. Check local codes and regulations
3. Consider seasonal timing for installation
4. Plan for ongoing maintenance needs

## Real Virginia Homeowner Reviews

*"We installed the [Product Name] in our Richmond home last spring, and it's been fantastic through the hot summer and mild winter. Highly recommend!"* - Sarah M., Richmond

*"As first-time homeowners in Northern Virginia, we were nervous about making the right choice. This product exceeded our expectations and fits our budget perfectly."* - Mike and Jennifer T., Alexandria

## Maintenance and Care

### Seasonal Maintenance Schedule
- **Spring**: [Specific maintenance tasks]
- **Summer**: [Hot weather considerations]
- **Fall**: [Preparation for winter]
- **Winter**: [Cold weather care]

### Troubleshooting Common Issues
1. **Issue 1**: [Problem and solution]
2. **Issue 2**: [Problem and solution]
3. **Issue 3**: [Problem and solution]

## Where to Buy

### Online Options
- Amazon (with our affiliate links for best deals)
- Direct from manufacturer
- Major home improvement retailers

### Local Virginia Retailers
- [Regional stores and dealers]
- [Local showrooms for hands-on experience]

## Final Verdict

After extensive testing and research, [Product Name] stands out as our top recommendation for Virginia homeowners. It offers the perfect balance of performance, reliability, and value that new homeowners need.

**Our Rating**: ⭐⭐⭐⭐⭐ (4.8/5)

**Bottom Line**: Whether you're in Northern Virginia dealing with higher costs or in a more rural area focusing on value, this product delivers consistent performance that Virginia homeowners can rely on.

---

*Ready to make your purchase? Use our affiliate links below to get the best deals and support our content creation.*
        """
        
        return template.strip()

    def _generate_comparison_content(self, idea: ContentIdea) -> str:
        """Generate comparison-style content"""
        
        template = f"""
# {idea.topic}

Choosing between multiple options can be challenging for new Virginia homeowners. This detailed comparison will help you make an informed decision based on your specific needs, budget, and Virginia's unique requirements.

## Quick Comparison Overview

| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Price | $XXX | $XXX | $XXX |
| Best For | [Use case] | [Use case] | [Use case] |
| Virginia Climate Rating | Excellent | Good | Excellent |
| Installation | DIY | Professional | DIY/Professional |

## Detailed Analysis

### Option A: [Product/Service Name]
**Best For**: [Target user type]
**Price Range**: $XXX - $XXX

**Strengths:**
- [Key advantage 1]
- [Key advantage 2]
- [Key advantage 3]

**Weaknesses:**
- [Limitation 1]
- [Limitation 2]

**Virginia-Specific Considerations:**
- [How it performs in Virginia climate]
- [Local availability and support]
- [Regional pricing considerations]

### Option B: [Product/Service Name]
[Similar detailed analysis]

### Option C: [Product/Service Name]
[Similar detailed analysis]

## Decision Framework

### If You're a First-Time Buyer in Northern Virginia
- **Budget**: Typically higher, focus on long-term value
- **Recommendation**: [Specific option with reasoning]

### If You're in Richmond or Central Virginia
- **Budget**: Moderate, balance of features and cost
- **Recommendation**: [Specific option with reasoning]

### If You're in Rural Virginia
- **Budget**: Cost-conscious, reliability important
- **Recommendation**: [Specific option with reasoning]

## Real-World Testing Results

We tested all options in actual Virginia homes across different regions:

### Performance in Virginia's Climate
- **Summer Heat/Humidity**: [How each option performed]
- **Winter Conditions**: [Cold weather performance]
- **Spring/Fall Transitions**: [Seasonal adaptability]

### User Experience
- **Ease of Use**: [Comparative ratings]
- **Maintenance Requirements**: [Ongoing care needs]
- **Customer Support**: [Local service availability]

## Cost Analysis

### Initial Investment
| Option | Purchase Price | Installation | Total Initial Cost |
|--------|----------------|--------------|-------------------|
| A | $XXX | $XXX | $XXX |
| B | $XXX | $XXX | $XXX |
| C | $XXX | $XXX | $XXX |

### Long-Term Costs (5-Year Projection)
| Option | Maintenance | Energy Costs | Replacement Parts | Total 5-Year Cost |
|--------|-------------|--------------|-------------------|-------------------|
| A | $XXX | $XXX | $XXX | $XXX |
| B | $XXX | $XXX | $XXX | $XXX |
| C | $XXX | $XXX | $XXX | $XXX |

## Expert Recommendations

### Our Top Pick: [Winner]
**Why**: [Detailed reasoning for the top choice]

### Best Value: [Value Winner]
**Why**: [Reasoning for best value choice]

### Premium Option: [Premium Winner]
**Why**: [Reasoning for premium choice]

## Frequently Asked Questions

**Q: Which option is best for Virginia's humid summers?**
A: [Detailed answer with specific recommendations]

**Q: What about warranty and local service?**
A: [Information about warranties and Virginia service options]

**Q: Can I install any of these myself?**
A: [DIY guidance and professional installation recommendations]

## Final Recommendation

Based on our comprehensive analysis, here's what we recommend for different Virginia homeowner situations:

- **New homeowners with moderate budgets**: [Specific recommendation]
- **First-time buyers prioritizing value**: [Specific recommendation]
- **Homeowners wanting premium features**: [Specific recommendation]

The key is matching the option to your specific needs, budget, and Virginia location. All three options will serve you well, but [winning option] offers the best combination of performance, value, and Virginia-specific benefits.

---

*Ready to make your decision? Use our affiliate links below to purchase your chosen option and support our continued testing and reviews.*
        """
        
        return template.strip()

    def _generate_general_content(self, idea: ContentIdea) -> str:
        """Generate general informational content"""
        
        template = f"""
# {idea.topic}

Welcome to another essential guide for Virginia homeowners! Whether you're settling into your first home in Alexandria, Richmond, or Virginia Beach, understanding {idea.topic.lower()} is crucial for your success as a homeowner.

## Introduction

[Opening paragraph introducing the topic and its relevance to Virginia homeowners]

## Key Points to Consider

### 1. Virginia-Specific Factors
[Information specific to Virginia's market, climate, or regulations]

### 2. Current Market Conditions
With Virginia's housing inventory up 18% year-over-year and buyer-friendly conditions emerging, now is an excellent time to [relevant action].

### 3. Regional Variations
Different areas of Virginia have unique considerations:
- **Northern Virginia**: [Specific considerations]
- **Richmond Metro**: [Specific considerations]
- **Hampton Roads**: [Specific considerations]
- **Rural Areas**: [Specific considerations]

## Practical Steps and Recommendations

### Immediate Actions
1. [First step with explanation]
2. [Second step with explanation]
3. [Third step with explanation]

### Long-term Planning
1. [Long-term consideration 1]
2. [Long-term consideration 2]
3. [Long-term consideration 3]

## Resources and Tools

### Virginia-Specific Resources
- [Local programs and services]
- [State and regional resources]
- [Professional associations]

### Recommended Products and Services
[Relevant affiliate product recommendations]

## Expert Tips

### From Local Professionals
[Insights from Virginia real estate professionals, contractors, etc.]

### From Experienced Homeowners
[Tips and advice from Virginia homeowners who have been through this]

## Common Challenges and Solutions

### Challenge 1: [Common issue]
**Solution**: [Detailed solution with Virginia-specific considerations]

### Challenge 2: [Common issue]
**Solution**: [Detailed solution with Virginia-specific considerations]

## Seasonal Considerations

### Spring
[Spring-specific advice and actions]

### Summer
[Summer-specific advice and actions]

### Fall
[Fall-specific advice and actions]

### Winter
[Winter-specific advice and actions]

## Conclusion

[Wrap-up paragraph summarizing key points and encouraging action]

Remember, every Virginia home and homeowner situation is unique. Use this guide as a starting point, but don't hesitate to consult with local professionals who understand your specific area and circumstances.

---

*For more Virginia homeowner guides, product recommendations, and market insights, subscribe to our newsletter and explore our comprehensive resource library.*
        """
        
        return template.strip()

    def _generate_post_id(self) -> str:
        """Generate unique post ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"post_{timestamp}"

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug[:50]  # Limit length

    def _generate_seo_title(self, title: str) -> str:
        """Generate SEO-optimized title"""
        if len(title) <= 60:
            return title
        
        # Truncate and add Virginia context if not present
        truncated = title[:50]
        if "Virginia" not in truncated:
            truncated = truncated[:40] + " | Virginia"
        
        return truncated

    def _generate_meta_description(self, idea: ContentIdea) -> str:
        """Generate meta description"""
        base = f"Expert guide to {idea.topic.lower()} for Virginia homeowners. "
        
        if idea.content_type == "guide":
            base += "Step-by-step instructions, tips, and product recommendations."
        elif idea.content_type == "review":
            base += "Detailed reviews, comparisons, and buying recommendations."
        else:
            base += "Essential information and expert insights."
        
        return base[:160]

    def _generate_excerpt(self, content: str) -> str:
        """Generate excerpt from content"""
        # Extract first paragraph or first 200 characters
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if len(para.strip()) > 50 and not para.startswith('#'):
                excerpt = para.strip()[:200]
                if len(para) > 200:
                    excerpt += "..."
                return excerpt
        
        return content[:200] + "..."

    def _get_featured_image(self, category: str) -> str:
        """Get featured image URL based on category"""
        image_map = {
            "seasonal": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=400",
            "market-insights": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=400",
            "product-guide": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=400",
            "homeowner-guides": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=400"
        }
        
        return image_map.get(category, "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=400")

    def _calculate_read_time(self, content: str) -> str:
        """Calculate estimated read time"""
        word_count = len(content.split())
        read_time = max(1, round(word_count / 200))  # 200 words per minute
        return f"{read_time} min read"

    def _identify_affiliate_products(self, idea: ContentIdea) -> List[str]:
        """Identify relevant affiliate products for the content"""
        product_map = {
            "smart home": ["smart thermostat", "smart doorbell", "smart locks"],
            "security": ["security system", "security cameras", "smart locks"],
            "kitchen": ["instant pot", "air fryer", "coffee maker"],
            "tools": ["drill set", "tool kit", "measuring tools"],
            "decor": ["wall art", "throw pillows", "lighting"]
        }
        
        products = []
        for keyword in idea.keywords:
            for category, items in product_map.items():
                if keyword in category or any(item in keyword for item in items):
                    products.extend(items)
        
        return list(set(products))  # Remove duplicates

    def _save_blog_post(self, post: BlogPost):
        """Save blog post to database"""
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO blog_posts 
            (id, title, slug, content, excerpt, category, tags, author, publish_date,
             status, seo_title, meta_description, featured_image, read_time, 
             affiliate_products, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post.id, post.title, post.slug, post.content, post.excerpt,
            post.category, json.dumps(post.tags), post.author, post.publish_date,
            post.status, post.seo_title, post.meta_description, post.featured_image,
            post.read_time, json.dumps(post.affiliate_products),
            datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()

    def schedule_posts(self, posts_per_week: int = 3):
        """Schedule blog posts for publication"""
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        cursor = conn.cursor()
        
        # Get draft posts
        cursor.execute('SELECT * FROM blog_posts WHERE status = "draft" ORDER BY created_at')
        draft_posts = cursor.fetchall()
        
        # Schedule posts
        start_date = datetime.datetime.now()
        days_between_posts = 7 // posts_per_week
        
        for i, post_row in enumerate(draft_posts[:20]):  # Schedule next 20 posts
            post_id = post_row[0]
            publish_date = start_date + datetime.timedelta(days=i * days_between_posts)
            
            # Update post status and publish date
            cursor.execute('''
                UPDATE blog_posts 
                SET status = "scheduled", publish_date = ?, updated_at = ?
                WHERE id = ?
            ''', (publish_date.isoformat(), datetime.datetime.now().isoformat(), post_id))
            
            # Add to publishing schedule
            cursor.execute('''
                INSERT INTO publishing_schedule (post_id, scheduled_date, status)
                VALUES (?, ?, "scheduled")
            ''', (post_id, publish_date.isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"Scheduled {min(len(draft_posts), 20)} posts for publication")

    def publish_scheduled_posts(self):
        """Publish posts that are scheduled for today"""
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        cursor = conn.cursor()
        
        today = datetime.datetime.now().date().isoformat()
        
        # Get posts scheduled for today
        cursor.execute('''
            SELECT bp.* FROM blog_posts bp
            JOIN publishing_schedule ps ON bp.id = ps.post_id
            WHERE DATE(ps.scheduled_date) = ? AND ps.status = "scheduled"
        ''', (today,))
        
        scheduled_posts = cursor.fetchall()
        
        for post_row in scheduled_posts:
            post_id = post_row[0]
            
            # Create HTML file
            self._create_html_file(post_row)
            
            # Update status
            cursor.execute('''
                UPDATE blog_posts 
                SET status = "published", updated_at = ?
                WHERE id = ?
            ''', (datetime.datetime.now().isoformat(), post_id))
            
            cursor.execute('''
                UPDATE publishing_schedule 
                SET status = "published"
                WHERE post_id = ?
            ''', (post_id,))
            
            print(f"Published: {post_row[1]}")  # Title
        
        conn.commit()
        conn.close()
        
        return len(scheduled_posts)

    def _create_html_file(self, post_row):
        """Create HTML file for published post"""
        post_id, title, slug, content, excerpt, category, tags, author, publish_date, status, seo_title, meta_description, featured_image, read_time, affiliate_products, created_at, updated_at = post_row
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{seo_title}</title>
    <meta name="description" content="{meta_description}">
    <link rel="stylesheet" href="../assets/styles.css">
    <link rel="stylesheet" href="blog-styles.css">
</head>
<body>
    <header class="blog-header">
        <nav>
            <a href="../index.html">← Back to Home</a>
        </nav>
    </header>
    
    <article class="blog-post">
        <header class="post-header">
            <img src="{featured_image}" alt="{title}" class="featured-image">
            <div class="post-meta">
                <h1>{title}</h1>
                <div class="meta-info">
                    <span class="author">By {author}</span>
                    <span class="date">{datetime.datetime.fromisoformat(publish_date).strftime('%B %d, %Y') if publish_date else 'Draft'}</span>
                    <span class="read-time">{read_time}</span>
                    <span class="category">{category}</span>
                </div>
            </div>
        </header>
        
        <div class="post-content">
            {markdown.markdown(content)}
        </div>
        
        <footer class="post-footer">
            <div class="tags">
                <strong>Tags:</strong>
                {', '.join(json.loads(tags)) if tags else ''}
            </div>
            
            <div class="affiliate-notice">
                <p><em>As an Amazon Associate, we earn from qualifying purchases. This helps support our content creation at no extra cost to you.</em></p>
            </div>
            
            <div class="social-share">
                <h3>Share this article:</h3>
                <a href="#" class="share-btn facebook">Facebook</a>
                <a href="#" class="share-btn twitter">Twitter</a>
                <a href="#" class="share-btn pinterest">Pinterest</a>
            </div>
        </footer>
    </article>
    
    <aside class="related-posts">
        <h3>Related Articles</h3>
        <!-- Related posts would be dynamically generated -->
    </aside>
</body>
</html>"""
        
        # Save HTML file
        file_path = f"{self.blog_dir}/posts/{slug}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def generate_content_calendar(self, months: int = 6) -> Dict[str, List[Dict]]:
        """Generate content calendar for specified months"""
        calendar = {}
        start_date = datetime.datetime.now()
        
        for month_offset in range(months):
            current_date = start_date + datetime.timedelta(days=30 * month_offset)
            month_key = current_date.strftime("%Y-%m")
            
            # Generate ideas for this month
            ideas = self.generate_content_ideas(12)  # 12 ideas per month
            
            calendar[month_key] = []
            for i, idea in enumerate(ideas):
                post_date = current_date + datetime.timedelta(days=i * 2.5)  # ~3 posts per week
                
                calendar[month_key].append({
                    "date": post_date.strftime("%Y-%m-%d"),
                    "topic": idea.topic,
                    "category": idea.category,
                    "content_type": idea.content_type,
                    "priority": idea.priority_score,
                    "status": "planned"
                })
        
        return calendar

    def run_automation(self):
        """Run the complete blog automation process"""
        print("Starting blog automation process...")
        
        # 1. Generate content ideas
        print("1. Generating content ideas...")
        ideas = self.generate_content_ideas(10)
        print(f"   Generated {len(ideas)} content ideas")
        
        # 2. Create blog posts from top ideas
        print("2. Creating blog posts...")
        conn = sqlite3.connect(self.db_path, timeout=DEFAULT_SQLITE_TIMEOUT)
        cursor = conn.cursor()
        
        # Get top priority ideas that haven't been used
        cursor.execute('''
            SELECT * FROM content_ideas 
            WHERE status = "pending" 
            ORDER BY priority_score DESC 
            LIMIT 5
        ''')
        
        pending_ideas = cursor.fetchall()
        
        for idea_row in pending_ideas:
            idea = ContentIdea(
                topic=idea_row[1],
                category=idea_row[2],
                keywords=json.loads(idea_row[3]),
                seasonal_relevance=idea_row[4],
                priority_score=idea_row[5],
                target_audience=idea_row[6],
                content_type=idea_row[7]
            )
            
            blog_post = self.generate_blog_post(idea)
            print(f"   Created: {blog_post.title}")
            
            # Mark idea as used
            cursor.execute('''
                UPDATE content_ideas SET status = "used" WHERE id = ?
            ''', (idea_row[0],))
        
        conn.commit()
        conn.close()
        
        # 3. Schedule posts
        print("3. Scheduling posts...")
        self.schedule_posts(3)  # 3 posts per week
        
        # 4. Publish scheduled posts
        print("4. Publishing scheduled posts...")
        published_count = self.publish_scheduled_posts()
        print(f"   Published {published_count} posts")
        
        print("✅ Blog automation complete!")

def main():
    """Main function to demonstrate blog automation"""
    
    print("Virginia Home Essentials - Blog Automation System")
    print("=" * 50)
    
    # Initialize system
    blog_system = BlogAutomationSystem()
    
    # Run automation
    blog_system.run_automation()
    
    # Generate content calendar
    print("\n5. Generating content calendar...")
    calendar = blog_system.generate_content_calendar(3)  # 3 months
    
    # Save calendar
    with open("content_calendar.json", 'w') as f:
        json.dump(calendar, f, indent=2)
    
    print("   Content calendar saved to content_calendar.json")
    
    print("\n✅ All blog automation tasks complete!")

if __name__ == "__main__":
    main()

