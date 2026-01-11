#!/usr/bin/env python3
"""
Virginia Home Essentials - Product Tracker
Automated system for tracking trending products, prices, and affiliate opportunities
"""

import requests
import json
import csv
import datetime
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
import os
from bs4 import BeautifulSoup
import re

@dataclass
class Product:
    asin: str
    title: str
    price: float
    rating: float
    review_count: int
    category: str
    image_url: str
    affiliate_url: str
    last_updated: str
    trending_score: float
    availability: str
    prime_eligible: bool

@dataclass
class TrendingProduct:
    keyword: str
    search_volume: int
    competition_level: str
    seasonal_trend: str
    recommended_products: List[str]

class AmazonProductTracker:
    def __init__(self, associate_tag: str = "your-tag-20"):
        """Initialize the product tracker"""
        self.associate_tag = associate_tag
        self.db_path = "products.db"
        self.init_database()
        
        # Virginia-specific product categories for new homeowners
        self.target_categories = {
            "smart_home": [
                "smart thermostat", "smart doorbell", "smart locks", "smart lights",
                "smart plugs", "smart speakers", "home automation", "smart security"
            ],
            "security": [
                "home security system", "security cameras", "motion sensors",
                "door sensors", "window alarms", "smart locks", "doorbell camera"
            ],
            "kitchen": [
                "instant pot", "air fryer", "coffee maker", "blender", "food processor",
                "kitchen appliances", "cookware set", "kitchen tools"
            ],
            "tools": [
                "drill set", "tool kit", "screwdriver set", "hammer", "measuring tape",
                "level", "utility knife", "toolbox", "home repair tools"
            ],
            "decor": [
                "wall art", "throw pillows", "curtains", "rugs", "lighting",
                "storage solutions", "shelving", "home decor"
            ],
            "seasonal": [
                "humidifier", "dehumidifier", "space heater", "fan", "air purifier",
                "seasonal decor", "outdoor furniture", "garden tools"
            ]
        }
        
        # Headers for web scraping (rotate these)
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        ]

    def init_database(self):
        """Initialize SQLite database for product tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                asin TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL,
                rating REAL,
                review_count INTEGER,
                category TEXT,
                image_url TEXT,
                affiliate_url TEXT,
                last_updated TEXT,
                trending_score REAL,
                availability TEXT,
                prime_eligible BOOLEAN
            )
        ''')
        
        # Price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT,
                price REAL,
                timestamp TEXT,
                FOREIGN KEY (asin) REFERENCES products (asin)
            )
        ''')
        
        # Trending keywords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trending_keywords (
                keyword TEXT PRIMARY KEY,
                search_volume INTEGER,
                competition_level TEXT,
                seasonal_trend TEXT,
                last_updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def search_amazon_products(self, keyword: str, category: str, max_results: int = 20) -> List[Product]:
        """Search for products on Amazon (simulated - would use actual API in production)"""
        
        # In production, this would use Amazon Product Advertising API
        # For now, we'll simulate with realistic data
        
        simulated_products = self._get_simulated_products(keyword, category, max_results)
        
        # Save to database
        self._save_products_to_db(simulated_products)
        
        return simulated_products

    def _get_simulated_products(self, keyword: str, category: str, max_results: int) -> List[Product]:
        """Generate simulated product data based on our research"""
        
        # Base products from our research
        base_products = {
            "smart thermostat": [
                {
                    "title": "Nest Learning Thermostat - Smart WiFi Thermostat",
                    "price": 249.99,
                    "rating": 4.3,
                    "review_count": 67543,
                    "prime_eligible": True
                },
                {
                    "title": "Ecobee SmartThermostat with Voice Control",
                    "price": 199.99,
                    "rating": 4.4,
                    "review_count": 45678,
                    "prime_eligible": True
                }
            ],
            "smart doorbell": [
                {
                    "title": "Ring Video Doorbell - 1080p HD Video",
                    "price": 99.99,
                    "rating": 4.4,
                    "review_count": 156789,
                    "prime_eligible": True
                },
                {
                    "title": "Arlo Essential Video Doorbell - Wire-Free",
                    "price": 149.99,
                    "rating": 4.2,
                    "review_count": 34567,
                    "prime_eligible": True
                }
            ],
            "instant pot": [
                {
                    "title": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
                    "price": 79.95,
                    "rating": 4.7,
                    "review_count": 234567,
                    "prime_eligible": True
                },
                {
                    "title": "Instant Pot Pro 10-in-1 Pressure Cooker",
                    "price": 129.95,
                    "rating": 4.6,
                    "review_count": 89012,
                    "prime_eligible": True
                }
            ],
            "drill set": [
                {
                    "title": "BLACK+DECKER 20V MAX Cordless Drill",
                    "price": 49.99,
                    "rating": 4.3,
                    "review_count": 45678,
                    "prime_eligible": True
                },
                {
                    "title": "DEWALT 20V MAX Cordless Drill/Driver Kit",
                    "price": 99.99,
                    "rating": 4.6,
                    "review_count": 78901,
                    "prime_eligible": True
                }
            ]
        }
        
        products = []
        base_data = base_products.get(keyword, [])
        
        for i, product_data in enumerate(base_data[:max_results]):
            asin = f"B{str(hash(keyword + str(i)))[-9:]}"
            
            product = Product(
                asin=asin,
                title=product_data["title"],
                price=product_data["price"],
                rating=product_data["rating"],
                review_count=product_data["review_count"],
                category=category,
                image_url=f"https://images.unsplash.com/photo-{1500000000 + i}?w=400&h=400",
                affiliate_url=f"https://amazon.com/dp/{asin}?tag={self.associate_tag}",
                last_updated=datetime.datetime.now().isoformat(),
                trending_score=self._calculate_trending_score(product_data),
                availability="In Stock",
                prime_eligible=product_data["prime_eligible"]
            )
            
            products.append(product)
        
        return products

    def _calculate_trending_score(self, product_data: Dict) -> float:
        """Calculate trending score based on rating, reviews, and other factors"""
        
        rating_score = product_data["rating"] / 5.0  # Normalize to 0-1
        review_score = min(product_data["review_count"] / 100000, 1.0)  # Cap at 100k reviews
        prime_score = 0.1 if product_data["prime_eligible"] else 0.0
        
        trending_score = (rating_score * 0.4) + (review_score * 0.4) + prime_score + 0.1
        
        return round(trending_score, 2)

    def _save_products_to_db(self, products: List[Product]):
        """Save products to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for product in products:
            # Insert or update product
            cursor.execute('''
                INSERT OR REPLACE INTO products 
                (asin, title, price, rating, review_count, category, image_url, 
                 affiliate_url, last_updated, trending_score, availability, prime_eligible)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product.asin, product.title, product.price, product.rating,
                product.review_count, product.category, product.image_url,
                product.affiliate_url, product.last_updated, product.trending_score,
                product.availability, product.prime_eligible
            ))
            
            # Add price history
            cursor.execute('''
                INSERT INTO price_history (asin, price, timestamp)
                VALUES (?, ?, ?)
            ''', (product.asin, product.price, product.last_updated))
        
        conn.commit()
        conn.close()

    def get_trending_products(self, category: str = None, limit: int = 10) -> List[Product]:
        """Get trending products from database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT * FROM products 
                WHERE category = ? 
                ORDER BY trending_score DESC, review_count DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM products 
                ORDER BY trending_score DESC, review_count DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            product = Product(
                asin=row[0], title=row[1], price=row[2], rating=row[3],
                review_count=row[4], category=row[5], image_url=row[6],
                affiliate_url=row[7], last_updated=row[8], trending_score=row[9],
                availability=row[10], prime_eligible=bool(row[11])
            )
            products.append(product)
        
        return products

    def update_all_products(self):
        """Update all products in database with current data"""
        
        print("Starting product update process...")
        
        for category, keywords in self.target_categories.items():
            print(f"\nUpdating {category} products...")
            
            for keyword in keywords:
                print(f"  Searching for: {keyword}")
                
                try:
                    products = self.search_amazon_products(keyword, category, 5)
                    print(f"    Found {len(products)} products")
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    Error searching for {keyword}: {e}")
                    continue
        
        print("\n✅ Product update complete!")

    def generate_product_report(self, output_file: str = "product_report.json"):
        """Generate comprehensive product report"""
        
        report = {
            "generated_at": datetime.datetime.now().isoformat(),
            "categories": {},
            "top_trending": [],
            "price_alerts": [],
            "new_products": []
        }
        
        # Get products by category
        for category in self.target_categories.keys():
            products = self.get_trending_products(category, 10)
            report["categories"][category] = [asdict(p) for p in products]
        
        # Get overall top trending
        top_products = self.get_trending_products(limit=20)
        report["top_trending"] = [asdict(p) for p in top_products]
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Product report saved to {output_file}")
        
        return report

    def export_products_for_website(self, output_file: str = "../assets/products.json"):
        """Export products in format suitable for website"""
        
        website_data = {}
        
        for category in self.target_categories.keys():
            products = self.get_trending_products(category, 8)
            
            website_products = []
            for product in products:
                website_product = {
                    "id": hash(product.asin) % 10000,
                    "title": product.title,
                    "description": self._generate_product_description(product),
                    "price": f"${product.price:.2f}",
                    "rating": product.rating,
                    "reviews": f"{product.review_count:,}",
                    "image": product.image_url,
                    "amazonUrl": product.affiliate_url,
                    "category": category.replace("_", "-"),
                    "trending": product.trending_score > 0.7
                }
                website_products.append(website_product)
            
            website_data[category.replace("_", "-")] = website_products
        
        # Save for website
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(website_data, f, indent=2)
        
        print(f"Website products exported to {output_file}")
        
        return website_data

    def _generate_product_description(self, product: Product) -> str:
        """Generate product description for website"""
        
        descriptions = {
            "smart_home": "Perfect for automating your new Virginia home with smart technology",
            "security": "Essential security solution for protecting your new home and family",
            "kitchen": "Must-have kitchen appliance for new homeowners starting their culinary journey",
            "tools": "Essential tool for DIY projects and home maintenance tasks",
            "decor": "Beautiful home decor item to personalize your new living space",
            "seasonal": "Seasonal essential for Virginia's changing weather conditions"
        }
        
        base_description = descriptions.get(product.category, "Great addition to any new home")
        
        if product.prime_eligible:
            base_description += " - Prime eligible for fast delivery"
        
        if product.rating >= 4.5:
            base_description += " - Highly rated by customers"
        
        return base_description

    def monitor_price_changes(self, threshold_percent: float = 10.0) -> List[Dict]:
        """Monitor for significant price changes"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get products with price history
        cursor.execute('''
            SELECT p.asin, p.title, p.price as current_price, p.category,
                   ph.price as historical_price, ph.timestamp
            FROM products p
            JOIN price_history ph ON p.asin = ph.asin
            WHERE ph.timestamp < date('now', '-1 day')
            ORDER BY p.asin, ph.timestamp DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        price_alerts = []
        current_product = None
        
        for row in rows:
            asin, title, current_price, category, historical_price, timestamp = row
            
            if current_product != asin:
                current_product = asin
                
                if historical_price and current_price:
                    price_change = ((current_price - historical_price) / historical_price) * 100
                    
                    if abs(price_change) >= threshold_percent:
                        alert = {
                            "asin": asin,
                            "title": title,
                            "category": category,
                            "current_price": current_price,
                            "previous_price": historical_price,
                            "price_change_percent": round(price_change, 2),
                            "alert_type": "price_drop" if price_change < 0 else "price_increase"
                        }
                        price_alerts.append(alert)
        
        return price_alerts

def main():
    """Main function to demonstrate the product tracker"""
    
    print("Virginia Home Essentials - Product Tracker")
    print("=" * 50)
    
    # Initialize tracker
    tracker = AmazonProductTracker("virginiahomee-20")
    
    # Update all products
    print("\n1. Updating product database...")
    tracker.update_all_products()
    
    # Generate report
    print("\n2. Generating product report...")
    report = tracker.generate_product_report()
    
    # Export for website
    print("\n3. Exporting products for website...")
    website_data = tracker.export_products_for_website()
    
    # Check for price changes
    print("\n4. Monitoring price changes...")
    price_alerts = tracker.monitor_price_changes()
    
    if price_alerts:
        print(f"Found {len(price_alerts)} price alerts:")
        for alert in price_alerts[:5]:  # Show first 5
            print(f"  - {alert['title']}: {alert['price_change_percent']:.1f}% change")
    else:
        print("No significant price changes detected")
    
    print("\n✅ Product tracking complete!")
    print(f"Database contains products for {len(tracker.target_categories)} categories")

if __name__ == "__main__":
    main()

