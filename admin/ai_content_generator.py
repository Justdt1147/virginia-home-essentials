#!/usr/bin/env python3
"""
Virginia Home Essentials - AI Content Generator
Automated system for generating blog posts, product recommendations, and market insights
"""

import json
import requests
import datetime
import os
from typing import List, Dict, Any
import openai
from dataclasses import dataclass
import csv

@dataclass
class ProductRecommendation:
    title: str
    description: str
    category: str
    price_range: str
    amazon_search_terms: List[str]
    target_audience: str
    seasonal_relevance: str

@dataclass
class BlogPost:
    title: str
    content: str
    excerpt: str
    category: str
    keywords: List[str]
    target_audience: str
    estimated_read_time: str
    seo_meta: Dict[str, str]

class VirginiaHomeAI:
    def __init__(self, openai_api_key: str = None):
        """Initialize the AI content generator"""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        self.virginia_context = {
            "climate": "Humid subtropical with hot summers and mild winters",
            "housing_market": "Growing inventory, buyer-friendly conditions in 2025",
            "demographics": "Mix of urban (NoVA), suburban, and rural areas",
            "key_cities": ["Virginia Beach", "Norfolk", "Richmond", "Alexandria", "Newport News"],
            "first_time_buyer_programs": ["Virginia Housing (VHDA)", "USDA Rural Development", "VA Loans"],
            "seasonal_considerations": {
                "winter": "Heating efficiency, snow preparation",
                "spring": "Home maintenance, garden prep",
                "summer": "Cooling costs, humidity control",
                "fall": "Winterization, leaf management"
            }
        }
        
        self.product_categories = {
            "smart_home": ["Echo devices", "Smart thermostats", "Security cameras", "Smart locks"],
            "security": ["Home security systems", "Doorbell cameras", "Motion sensors", "Smart locks"],
            "kitchen": ["Instant Pot", "Air fryers", "Coffee makers", "Food processors"],
            "tools": ["Drill sets", "Tool kits", "Measuring tools", "Safety equipment"],
            "decor": ["Lighting", "Storage solutions", "Wall art", "Furniture"],
            "seasonal": ["Humidifiers", "Dehumidifiers", "Space heaters", "Fans"]
        }

    def generate_trending_products(self, category: str, count: int = 10) -> List[ProductRecommendation]:
        """Generate trending product recommendations for a specific category"""
        
        prompt = f"""
        Generate {count} trending product recommendations for new homeowners in Virginia in the {category} category.
        
        Context:
        - Target audience: New homeowners (0-3 years) in Virginia
        - Focus on practical, high-value items
        - Consider Virginia's climate and housing market
        - Include seasonal relevance
        - Price range should be accessible to first-time buyers
        
        For each product, provide:
        1. Product title (specific but not branded)
        2. Detailed description (benefits for new homeowners)
        3. Price range
        4. Amazon search terms (3-5 terms)
        5. Target audience specifics
        6. Seasonal relevance
        
        Format as JSON array with the specified fields.
        """
        
        try:
            if self.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                # Parse JSON response and convert to ProductRecommendation objects
                products_data = json.loads(content)
                
                return [ProductRecommendation(**product) for product in products_data]
            else:
                # Fallback to predefined recommendations
                return self._get_fallback_products(category, count)
                
        except Exception as e:
            print(f"Error generating products: {e}")
            return self._get_fallback_products(category, count)

    def generate_blog_post(self, topic: str, keywords: List[str], target_length: int = 1500) -> BlogPost:
        """Generate a comprehensive blog post"""
        
        current_date = datetime.datetime.now().strftime("%B %Y")
        
        prompt = f"""
        Write a comprehensive blog post for Virginia homeowners about: {topic}
        
        Requirements:
        - Target length: {target_length} words
        - Keywords to include: {', '.join(keywords)}
        - Audience: New homeowners in Virginia (0-3 years)
        - Include Virginia-specific information and context
        - Mention current market conditions (December 2025)
        - Include actionable advice and product recommendations
        - SEO-optimized with clear headings
        - Engaging and informative tone
        
        Virginia Context:
        {json.dumps(self.virginia_context, indent=2)}
        
        Structure:
        1. Engaging introduction
        2. Main content with 3-5 sections
        3. Virginia-specific tips
        4. Product recommendations with Amazon affiliate potential
        5. Conclusion with call-to-action
        
        Also provide:
        - SEO title (under 60 characters)
        - Meta description (under 160 characters)
        - Excerpt (2-3 sentences)
        - Estimated read time
        - Category classification
        """
        
        try:
            if self.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=3000
                )
                
                content = response.choices[0].message.content
                
                # Extract components from the response
                # This would need more sophisticated parsing in production
                return self._parse_blog_response(content, topic, keywords)
            else:
                return self._get_fallback_blog_post(topic, keywords)
                
        except Exception as e:
            print(f"Error generating blog post: {e}")
            return self._get_fallback_blog_post(topic, keywords)

    def generate_market_insights(self) -> Dict[str, Any]:
        """Generate current market insights for Virginia"""
        
        prompt = f"""
        Generate current real estate market insights for Virginia as of December 2025.
        
        Include:
        1. Current market conditions
        2. Trends affecting new homeowners
        3. Regional variations (NoVA, Richmond, Virginia Beach, etc.)
        4. First-time buyer opportunities
        5. Seasonal market patterns
        6. Interest rate impacts
        7. Inventory levels and buyer/seller dynamics
        
        Base insights on recent data:
        - 36,801 homes for sale (+18% YoY)
        - NoVA median prices around $1.25M
        - Inventory up 52.7% in Northern Virginia
        - Buyer's market conditions emerging
        
        Format as structured JSON with actionable insights.
        """
        
        try:
            if self.openai_api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6
                )
                
                return json.loads(response.choices[0].message.content)
            else:
                return self._get_fallback_market_insights()
                
        except Exception as e:
            print(f"Error generating market insights: {e}")
            return self._get_fallback_market_insights()

    def generate_seasonal_content_calendar(self, year: int = 2025) -> Dict[str, List[Dict]]:
        """Generate a content calendar with seasonal topics"""
        
        calendar = {
            "January": [
                {"topic": "New Year Home Organization Essentials", "category": "organization"},
                {"topic": "Winter Energy Efficiency Tips for Virginia Homes", "category": "energy"},
                {"topic": "Post-Holiday Home Security Review", "category": "security"}
            ],
            "February": [
                {"topic": "Valentine's Day Home Decor on a Budget", "category": "decor"},
                {"topic": "Preparing Your Virginia Home for Spring", "category": "maintenance"},
                {"topic": "Smart Home Upgrades for New Homeowners", "category": "smart-home"}
            ],
            "March": [
                {"topic": "Spring Cleaning Essentials and Tools", "category": "cleaning"},
                {"topic": "Virginia Garden Prep: Tools and Supplies", "category": "outdoor"},
                {"topic": "Home Maintenance Checklist for Spring", "category": "maintenance"}
            ],
            "April": [
                {"topic": "Easter Entertaining: Kitchen Essentials", "category": "kitchen"},
                {"topic": "Allergy Season: Air Quality Solutions", "category": "health"},
                {"topic": "Virginia Real Estate Market Spring Update", "category": "market"}
            ],
            "May": [
                {"topic": "Mother's Day Gift Ideas for the Home", "category": "gifts"},
                {"topic": "Outdoor Living Setup for Virginia Weather", "category": "outdoor"},
                {"topic": "First-Time Buyer's Guide to Virginia Markets", "category": "buying"}
            ],
            "June": [
                {"topic": "Summer Cooling Solutions for Virginia Homes", "category": "cooling"},
                {"topic": "Father's Day Tool Gift Guide", "category": "tools"},
                {"topic": "Wedding Season: Home Entertaining Essentials", "category": "entertaining"}
            ],
            "July": [
                {"topic": "4th of July Outdoor Entertaining Setup", "category": "outdoor"},
                {"topic": "Summer Energy Savings Tips", "category": "energy"},
                {"topic": "Mid-Year Virginia Housing Market Review", "category": "market"}
            ],
            "August": [
                {"topic": "Back-to-School Home Office Setup", "category": "office"},
                {"topic": "Late Summer Home Maintenance Tasks", "category": "maintenance"},
                {"topic": "Hurricane Preparedness for Virginia Homeowners", "category": "safety"}
            ],
            "September": [
                {"topic": "Fall Decorating Trends and Essentials", "category": "decor"},
                {"topic": "Preparing Your Home for Fall in Virginia", "category": "seasonal"},
                {"topic": "Labor Day Weekend Home Projects", "category": "diy"}
            ],
            "October": [
                {"topic": "Halloween Home Decor and Safety", "category": "seasonal"},
                {"topic": "Fall Home Maintenance Checklist", "category": "maintenance"},
                {"topic": "Virginia Real Estate Market Fall Update", "category": "market"}
            ],
            "November": [
                {"topic": "Thanksgiving Hosting Essentials", "category": "entertaining"},
                {"topic": "Winter Preparation for Virginia Homes", "category": "seasonal"},
                {"topic": "Black Friday Home Deals Strategy", "category": "shopping"}
            ],
            "December": [
                {"topic": "Holiday Decorating and Storage Solutions", "category": "seasonal"},
                {"topic": "Year-End Home Maintenance Review", "category": "maintenance"},
                {"topic": "New Year Home Goals and Planning", "category": "planning"}
            ]
        }
        
        return calendar

    def _get_fallback_products(self, category: str, count: int) -> List[ProductRecommendation]:
        """Fallback product recommendations when AI is unavailable"""
        
        fallback_products = {
            "smart_home": [
                ProductRecommendation(
                    title="Smart Thermostat with Learning Capability",
                    description="Programmable thermostat that learns your schedule and adjusts temperature automatically, perfect for Virginia's variable climate",
                    category="smart_home",
                    price_range="$200-300",
                    amazon_search_terms=["smart thermostat", "programmable thermostat", "nest thermostat", "ecobee thermostat"],
                    target_audience="New homeowners wanting energy efficiency",
                    seasonal_relevance="Year-round, especially valuable during Virginia's hot summers and cold winters"
                ),
                ProductRecommendation(
                    title="Voice-Controlled Smart Speaker Hub",
                    description="Central hub for controlling smart home devices, playing music, and getting weather updates",
                    category="smart_home",
                    price_range="$50-150",
                    amazon_search_terms=["amazon echo", "google nest", "smart speaker", "voice assistant"],
                    target_audience="Tech-savvy new homeowners",
                    seasonal_relevance="Year-round utility for home automation"
                )
            ],
            "security": [
                ProductRecommendation(
                    title="Wireless Home Security System",
                    description="Complete security system with door/window sensors, motion detectors, and smartphone alerts",
                    category="security",
                    price_range="$200-400",
                    amazon_search_terms=["home security system", "wireless alarm", "simplisafe", "ring alarm"],
                    target_audience="Safety-conscious new homeowners",
                    seasonal_relevance="Year-round security, especially important during vacation seasons"
                )
            ]
        }
        
        return fallback_products.get(category, [])[:count]

    def _get_fallback_blog_post(self, topic: str, keywords: List[str]) -> BlogPost:
        """Fallback blog post when AI is unavailable"""
        
        return BlogPost(
            title=f"{topic}: Essential Guide for Virginia Homeowners",
            content=f"Comprehensive guide about {topic} tailored for Virginia homeowners...",
            excerpt=f"Discover everything you need to know about {topic} as a new homeowner in Virginia.",
            category="home-essentials",
            keywords=keywords,
            target_audience="New Virginia homeowners",
            estimated_read_time="5-7 minutes",
            seo_meta={
                "title": f"{topic} Guide for Virginia Homeowners",
                "description": f"Complete {topic} guide for new homeowners in Virginia. Expert tips and product recommendations."
            }
        )

    def _get_fallback_market_insights(self) -> Dict[str, Any]:
        """Fallback market insights when AI is unavailable"""
        
        return {
            "current_conditions": "Buyer-friendly market with increasing inventory",
            "key_trends": [
                "Inventory up 18% year-over-year statewide",
                "Northern Virginia seeing 52.7% inventory increase",
                "First-time buyer programs expanding"
            ],
            "regional_insights": {
                "northern_virginia": "High-priced market but more options available",
                "richmond": "Balanced market with steady growth",
                "virginia_beach": "Coastal market with seasonal variations"
            },
            "recommendations": [
                "Take advantage of increased inventory",
                "Explore first-time buyer programs",
                "Consider energy-efficient homes for long-term savings"
            ]
        }

    def _parse_blog_response(self, content: str, topic: str, keywords: List[str]) -> BlogPost:
        """Parse AI response into BlogPost object"""
        
        # This would need more sophisticated parsing in production
        # For now, return a structured response
        
        return BlogPost(
            title=f"{topic}: Complete Guide for Virginia Homeowners",
            content=content,
            excerpt=content[:200] + "...",
            category="home-essentials",
            keywords=keywords,
            target_audience="New Virginia homeowners",
            estimated_read_time="6-8 minutes",
            seo_meta={
                "title": f"{topic} - Virginia Home Essentials",
                "description": f"Expert guide to {topic} for Virginia homeowners. Tips, recommendations, and local insights."
            }
        )

    def save_content_to_files(self, content_type: str, content: Any, filename: str = None):
        """Save generated content to appropriate files"""
        
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{content_type}_{timestamp}"
        
        output_dir = "../generated_content"
        os.makedirs(output_dir, exist_ok=True)
        
        if content_type == "blog_post":
            # Save as HTML file
            html_content = self._convert_blog_to_html(content)
            with open(f"{output_dir}/{filename}.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        
        elif content_type == "products":
            # Save as JSON
            products_data = [
                {
                    "title": p.title,
                    "description": p.description,
                    "category": p.category,
                    "price_range": p.price_range,
                    "amazon_search_terms": p.amazon_search_terms,
                    "target_audience": p.target_audience,
                    "seasonal_relevance": p.seasonal_relevance
                }
                for p in content
            ]
            
            with open(f"{output_dir}/{filename}.json", "w", encoding="utf-8") as f:
                json.dump(products_data, f, indent=2)
        
        elif content_type == "market_insights":
            # Save as JSON
            with open(f"{output_dir}/{filename}.json", "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        
        print(f"Content saved to {output_dir}/{filename}")

    def _convert_blog_to_html(self, blog_post: BlogPost) -> str:
        """Convert blog post to HTML format"""
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{blog_post.seo_meta['title']}</title>
    <meta name="description" content="{blog_post.seo_meta['description']}">
    <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
    <article class="blog-post">
        <header class="post-header">
            <h1>{blog_post.title}</h1>
            <div class="post-meta">
                <span>Category: {blog_post.category}</span>
                <span>Read time: {blog_post.estimated_read_time}</span>
                <span>Target: {blog_post.target_audience}</span>
            </div>
        </header>
        
        <div class="post-content">
            {blog_post.content}
        </div>
        
        <footer class="post-footer">
            <div class="keywords">
                <strong>Keywords:</strong> {', '.join(blog_post.keywords)}
            </div>
        </footer>
    </article>
</body>
</html>
        """
        
        return html_template

def main():
    """Main function to demonstrate the AI content generator"""
    
    # Initialize the AI system
    ai_generator = VirginiaHomeAI()
    
    print("Virginia Home Essentials - AI Content Generator")
    print("=" * 50)
    
    # Generate trending products
    print("\n1. Generating trending smart home products...")
    smart_home_products = ai_generator.generate_trending_products("smart_home", 5)
    ai_generator.save_content_to_files("products", smart_home_products, "smart_home_trending")
    
    # Generate blog post
    print("\n2. Generating blog post...")
    blog_post = ai_generator.generate_blog_post(
        "Essential Smart Home Devices for New Virginia Homeowners",
        ["smart home", "Virginia", "new homeowners", "home automation", "energy efficiency"]
    )
    ai_generator.save_content_to_files("blog_post", blog_post, "smart_home_essentials")
    
    # Generate market insights
    print("\n3. Generating market insights...")
    market_insights = ai_generator.generate_market_insights()
    ai_generator.save_content_to_files("market_insights", market_insights, "virginia_market_december_2025")
    
    # Generate content calendar
    print("\n4. Generating content calendar...")
    content_calendar = ai_generator.generate_seasonal_content_calendar(2025)
    ai_generator.save_content_to_files("market_insights", content_calendar, "content_calendar_2025")
    
    print("\n✅ Content generation complete!")
    print("Check the generated_content folder for output files.")

if __name__ == "__main__":
    main()

