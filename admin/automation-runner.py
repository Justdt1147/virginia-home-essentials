#!/usr/bin/env python3
"""
Virginia Home Essentials - Master Automation Runner
Orchestrates all AI systems: content generation, product tracking, and blog automation
"""

import os
import sys
import json
import datetime
import schedule
import time
import logging
from pathlib import Path
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_content_generator import VirginiaHomeAI
from product_tracker import AmazonProductTracker
from blog_automation import BlogAutomationSystem

class MasterAutomationSystem:
    def __init__(self, config_file: str = "automation_config.json"):
        """Initialize the master automation system"""
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        
        # Initialize subsystems with proper error handling for missing API keys
        openai_key = self.config.get('openai_api_key')
        if not openai_key:
            self.logger.warning("OPENAI_API_KEY not configured. AI features will be limited.")
        
        self.ai_generator = VirginiaHomeAI(openai_key)
        self.product_tracker = AmazonProductTracker(self.config.get('amazon_associate_tag', 'virginiahomee-20'))
        self.blog_system = BlogAutomationSystem(openai_key)
        
        # Automation status
        self.last_run = {}
        self.load_status()

    def load_config(self) -> dict:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "openai_api_key": os.getenv('OPENAI_API_KEY', ''),
                "amazon_associate_tag": "virginiahomee-20",
                "automation_schedule": {
                    "content_generation": "daily",
                    "product_tracking": "daily", 
                    "blog_publishing": "daily",
                    "full_update": "weekly"
                },
                "content_settings": {
                    "posts_per_week": 3,
                    "products_per_category": 10,
                    "seasonal_content_ratio": 0.3
                },
                "notification_settings": {
                    "email_alerts": False,
                    "slack_webhook": "",
                    "discord_webhook": ""
                }
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/automation_{datetime.date.today()}.log"),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("MasterAutomation")

    def load_status(self):
        """Load last run status"""
        status_file = "automation_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                self.last_run = json.load(f)
        else:
            self.last_run = {
                "content_generation": None,
                "product_tracking": None,
                "blog_publishing": None,
                "full_update": None
            }

    def save_status(self):
        """Save current run status"""
        with open("automation_status.json", 'w') as f:
            json.dump(self.last_run, f, indent=2)

    def run_content_generation(self):
        """Run AI content generation tasks"""
        self.logger.info("Starting content generation...")
        
        try:
            # Generate trending products for all categories
            categories = ["smart_home", "security", "kitchen", "tools", "decor"]
            
            for category in categories:
                self.logger.info(f"Generating products for {category}...")
                products = self.ai_generator.generate_trending_products(category, 5)
                self.ai_generator.save_content_to_files("products", products, f"{category}_trending")
            
            # Generate market insights
            self.logger.info("Generating market insights...")
            insights = self.ai_generator.generate_market_insights()
            self.ai_generator.save_content_to_files("market_insights", insights, f"market_insights_{datetime.date.today()}")
            
            # Generate seasonal content calendar
            self.logger.info("Updating content calendar...")
            calendar = self.ai_generator.generate_seasonal_content_calendar()
            self.ai_generator.save_content_to_files("market_insights", calendar, "content_calendar_updated")
            
            self.last_run["content_generation"] = datetime.datetime.now().isoformat()
            self.logger.info("✅ Content generation completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Content generation failed: {e}")
            raise

    def run_product_tracking(self):
        """Run product tracking and updates"""
        self.logger.info("Starting product tracking...")
        
        try:
            # Update all products
            self.product_tracker.update_all_products()
            
            # Generate product report
            report = self.product_tracker.generate_product_report(f"reports/product_report_{datetime.date.today()}.json")
            
            # Export for website
            self.product_tracker.export_products_for_website()
            
            # Check for price alerts
            price_alerts = self.product_tracker.monitor_price_changes()
            if price_alerts:
                self.logger.info(f"Found {len(price_alerts)} price alerts")
                self.send_price_alerts(price_alerts)
            
            self.last_run["product_tracking"] = datetime.datetime.now().isoformat()
            self.logger.info("✅ Product tracking completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Product tracking failed: {e}")
            raise

    def run_blog_automation(self):
        """Run blog automation tasks"""
        self.logger.info("Starting blog automation...")
        
        try:
            # Run full blog automation
            self.blog_system.run_automation()
            
            self.last_run["blog_publishing"] = datetime.datetime.now().isoformat()
            self.logger.info("✅ Blog automation completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Blog automation failed: {e}")
            raise

    def run_full_update(self):
        """Run complete system update"""
        self.logger.info("Starting full system update...")
        
        try:
            # Run all subsystems
            self.run_content_generation()
            self.run_product_tracking()
            self.run_blog_automation()
            
            # Generate comprehensive reports
            self.generate_system_report()
            
            # Update website files
            self.update_website_files()
            
            self.last_run["full_update"] = datetime.datetime.now().isoformat()
            self.logger.info("✅ Full system update completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Full system update failed: {e}")
            raise

    def generate_system_report(self):
        """Generate comprehensive system report"""
        self.logger.info("Generating system report...")
        
        report = {
            "generated_at": datetime.datetime.now().isoformat(),
            "system_status": {
                "content_generation": self.last_run.get("content_generation"),
                "product_tracking": self.last_run.get("product_tracking"),
                "blog_publishing": self.last_run.get("blog_publishing"),
                "full_update": self.last_run.get("full_update")
            },
            "statistics": {
                "total_products_tracked": self.get_product_count(),
                "total_blog_posts": self.get_blog_post_count(),
                "scheduled_posts": self.get_scheduled_post_count()
            },
            "next_scheduled_runs": self.get_next_scheduled_runs()
        }
        
        # Save report
        os.makedirs("reports", exist_ok=True)
        report_file = f"reports/system_report_{datetime.date.today()}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"System report saved to {report_file}")

    def update_website_files(self):
        """Update website with latest content"""
        self.logger.info("Updating website files...")
        
        try:
            # Update product data for website
            self.product_tracker.export_products_for_website("../assets/products.json")
            
            # Update blog index
            self.update_blog_index()
            
            # Update market insights on homepage
            self.update_homepage_insights()
            
            self.logger.info("✅ Website files updated successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Website update failed: {e}")

    def update_blog_index(self):
        """Update blog index page with latest posts"""
        # This would generate an updated blog index page
        # For now, we'll create a simple JSON file with blog data
        
        import sqlite3
        conn = sqlite3.connect(self.blog_system.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, slug, excerpt, category, publish_date, featured_image, read_time
            FROM blog_posts 
            WHERE status = "published" 
            ORDER BY publish_date DESC 
            LIMIT 20
        ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        blog_data = []
        for post in posts:
            blog_data.append({
                "title": post[0],
                "slug": post[1],
                "excerpt": post[2],
                "category": post[3],
                "date": post[4],
                "image": post[5],
                "readTime": post[6],
                "url": f"blog/posts/{post[1]}.html"
            })
        
        with open("../assets/blog-posts.json", 'w') as f:
            json.dump(blog_data, f, indent=2)

    def update_homepage_insights(self):
        """Update homepage with latest market insights"""
        # This would update the homepage with fresh market data
        # For now, we'll create a JSON file with insights
        
        insights = self.ai_generator.generate_market_insights()
        
        with open("../assets/market-insights.json", 'w') as f:
            json.dump(insights, f, indent=2)

    def send_price_alerts(self, alerts: list):
        """Send price alerts via configured channels"""
        if not alerts:
            return
        
        alert_message = f"🚨 Price Alert: {len(alerts)} products have significant price changes:\n\n"
        
        for alert in alerts[:5]:  # Limit to top 5 alerts
            change_emoji = "📉" if alert["price_change_percent"] < 0 else "📈"
            alert_message += f"{change_emoji} {alert['title']}: {alert['price_change_percent']:.1f}% change\n"
        
        # Log alerts
        self.logger.info(f"Price alerts: {alert_message}")
        
        # Send notifications (implement based on config)
        if self.config.get("notification_settings", {}).get("email_alerts"):
            self.send_email_alert(alert_message)
        
        if self.config.get("notification_settings", {}).get("slack_webhook"):
            self.send_slack_alert(alert_message)

    def send_email_alert(self, message: str):
        """Send email alert (placeholder)"""
        # Implement email sending logic
        self.logger.info("Email alert would be sent here")

    def send_slack_alert(self, message: str):
        """Send Slack alert (placeholder)"""
        # Implement Slack webhook logic
        self.logger.info("Slack alert would be sent here")

    def get_product_count(self) -> int:
        """Get total number of tracked products"""
        import sqlite3
        conn = sqlite3.connect(self.product_tracker.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_blog_post_count(self) -> int:
        """Get total number of blog posts"""
        import sqlite3
        conn = sqlite3.connect(self.blog_system.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM blog_posts")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_scheduled_post_count(self) -> int:
        """Get number of scheduled posts"""
        import sqlite3
        conn = sqlite3.connect(self.blog_system.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM blog_posts WHERE status = "scheduled"')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_next_scheduled_runs(self) -> dict:
        """Get next scheduled run times"""
        # This would calculate next run times based on schedule
        # For now, return placeholder data
        return {
            "content_generation": "Tomorrow 9:00 AM",
            "product_tracking": "Tomorrow 10:00 AM", 
            "blog_publishing": "Tomorrow 11:00 AM",
            "full_update": "Next Sunday 8:00 AM"
        }

    def setup_scheduler(self):
        """Setup automated scheduling"""
        self.logger.info("Setting up automation scheduler...")
        
        # Daily tasks
        schedule.every().day.at("09:00").do(self.run_content_generation)
        schedule.every().day.at("10:00").do(self.run_product_tracking)
        schedule.every().day.at("11:00").do(self.run_blog_automation)
        
        # Weekly full update
        schedule.every().sunday.at("08:00").do(self.run_full_update)
        
        self.logger.info("✅ Scheduler configured")

    def run_scheduler(self):
        """Run the scheduler continuously"""
        self.logger.info("Starting automation scheduler...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
                # Save status periodically
                self.save_status()
                
            except KeyboardInterrupt:
                self.logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

    def run_manual_task(self, task: str):
        """Run a specific task manually"""
        self.logger.info(f"Running manual task: {task}")
        
        task_map = {
            "content": self.run_content_generation,
            "products": self.run_product_tracking,
            "blog": self.run_blog_automation,
            "full": self.run_full_update
        }
        
        if task in task_map:
            try:
                task_map[task]()
                self.save_status()
                self.logger.info(f"✅ Manual task '{task}' completed successfully")
            except Exception as e:
                self.logger.error(f"❌ Manual task '{task}' failed: {e}")
        else:
            self.logger.error(f"Unknown task: {task}")
            self.logger.info(f"Available tasks: {list(task_map.keys())}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Virginia Home Essentials - Master Automation System")
    parser.add_argument("--task", choices=["content", "products", "blog", "full", "schedule"], 
                       help="Run specific task or start scheduler")
    parser.add_argument("--config", default="automation_config.json", 
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    print("Virginia Home Essentials - Master Automation System")
    print("=" * 60)
    
    # Initialize system
    automation = MasterAutomationSystem(args.config)
    
    if args.task == "schedule":
        # Run continuous scheduler
        automation.setup_scheduler()
        automation.run_scheduler()
    elif args.task:
        # Run specific task
        automation.run_manual_task(args.task)
    else:
        # Interactive mode
        print("\nAvailable commands:")
        print("1. content  - Generate AI content and product recommendations")
        print("2. products - Update product tracking and pricing")
        print("3. blog     - Run blog automation and publishing")
        print("4. full     - Run complete system update")
        print("5. schedule - Start continuous automation scheduler")
        print("6. status   - Show system status")
        print("7. quit     - Exit")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "status":
                    automation.generate_system_report()
                    print("System status report generated")
                elif command in ["content", "products", "blog", "full"]:
                    automation.run_manual_task(command)
                elif command == "schedule":
                    automation.setup_scheduler()
                    automation.run_scheduler()
                    break
                else:
                    print("Unknown command. Try 'content', 'products', 'blog', 'full', 'schedule', 'status', or 'quit'")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    print("\n✅ Automation system shutdown complete")

if __name__ == "__main__":
    main()

