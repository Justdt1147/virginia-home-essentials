#!/usr/bin/env python3
"""
Sitemap Generator for Virginia Home Essentials
Automatically generates and updates sitemap.xml with blog posts
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path

def generate_sitemap(domain="https://yourdomain.com"):
    """Generate sitemap.xml with all pages and blog posts"""
    
    # Static pages
    static_urls = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/blog/", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/#products", "priority": "0.8", "changefreq": "daily"},
        {"loc": "/#market-insights", "priority": "0.7", "changefreq": "weekly"},
        {"loc": "/#about", "priority": "0.6", "changefreq": "monthly"},
    ]
    
    # Get blog posts from database
    blog_posts = []
    db_path = Path(__file__).parent / "admin" / "blog_system.db"
    
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path), timeout=30)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT slug, updated_at, status 
                FROM blog_posts 
                WHERE status = 'published'
                ORDER BY publish_date DESC
            """)
            
            for row in cursor.fetchall():
                slug, updated_at, status = row
                blog_posts.append({
                    "loc": f"/blog/{slug}.html",
                    "lastmod": updated_at.split('T')[0] if updated_at else datetime.now().strftime("%Y-%m-%d"),
                    "priority": "0.7",
                    "changefreq": "monthly"
                })
            
            conn.close()
        except Exception as e:
            print(f"Warning: Could not read blog posts from database: {e}")
    
    # Generate XML
    today = datetime.now().strftime("%Y-%m-%d")
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add static pages
    for url in static_urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{domain}{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{today}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    # Add blog posts
    for post in blog_posts:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{domain}{post["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{post["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{post["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{post["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>\n'
    
    # Write to file
    sitemap_path = Path(__file__).parent / "sitemap.xml"
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Sitemap generated with {len(static_urls)} static pages and {len(blog_posts)} blog posts")
    print(f"   Saved to: {sitemap_path}")
    
    return sitemap_path

if __name__ == "__main__":
    import sys
    
    # Allow custom domain as argument
    domain = sys.argv[1] if len(sys.argv) > 1 else "https://yourdomain.com"
    
    print("Virginia Home Essentials - Sitemap Generator")
    print("=" * 50)
    generate_sitemap(domain)
