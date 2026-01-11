#!/usr/bin/env python3
"""
Blog Export Utility - Virginia Home Essentials
Exports blog posts from database to JSON for website consumption
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

def export_blog_posts(output_file="../blog/posts.json", limit=50):
    """Export published blog posts to JSON file"""
    
    db_path = Path(__file__).parent / "blog_system.db"
    
    if not db_path.exists():
        print("⚠️  Blog database not found. Run blog automation first.")
        return
    
    try:
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, slug, excerpt, category, tags, author, 
                   publish_date, featured_image, read_time, updated_at
            FROM blog_posts 
            WHERE status = 'published'
            ORDER BY publish_date DESC
            LIMIT ?
        """, (limit,))
        
        posts = []
        for row in cursor.fetchall():
            post_id, title, slug, excerpt, category, tags, author, publish_date, featured_image, read_time, updated_at = row
            
            posts.append({
                "id": post_id,
                "title": title,
                "slug": slug,
                "excerpt": excerpt,
                "category": category,
                "tags": json.loads(tags) if tags else [],
                "author": author,
                "publish_date": publish_date,
                "featured_image": featured_image,
                "read_time": read_time,
                "updated_at": updated_at,
                "url": f"/blog/{slug}.html"
            })
        
        conn.close()
        
        # Write to JSON file
        output_path = Path(__file__).parent / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(posts)} blog posts to {output_path}")
        return posts
        
    except Exception as e:
        print(f"❌ Error exporting blog posts: {e}")
        return []

if __name__ == "__main__":
    import sys
    
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    
    print("Virginia Home Essentials - Blog Export")
    print("=" * 50)
    export_blog_posts(limit=limit)
