# Quick Start Guide
**Virginia Home Essentials - Get Running in 5 Minutes**

---

## 🚀 First-Time Setup

### 1. Install Dependencies
```bash
cd virginia-home-essentials
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the environment template
copy admin\.env.example .env

# Edit .env and add your keys:
# OPENAI_API_KEY=your-key-here (optional, has fallback)
# AMAZON_ASSOCIATE_TAG=virginiahomee-20 (already set)
```

### 3. Test the Website
```bash
# Start local web server
python -m http.server 8000

# Open browser to:
http://localhost:8000
```

✅ You should see the Virginia Home Essentials homepage with products!

---

## 🤖 Run Automation

### Option 1: Quick Test (Generate Content)
```bash
cd ..
.venv\Scripts\python.exe automation-runner.py --task full
```

This will:
- Generate trending products for 5 categories
- Create blog posts and market insights
- Update product tracking
- Export blog posts to JSON

### Option 2: Individual Tasks

**Generate Blog Posts Only:**
```bash
.venv\Scripts\python.exe automation-runner.py --task blog
```

**Update Products Only:**
```bash
.venv\Scripts\python.exe automation-runner.py --task products
```

**Generate Content Only:**
```bash
.venv\Scripts\python.exe automation-runner.py --task content
```

### Option 3: Scheduled Automation (Production)
```bash
.venv\Scripts\python.exe automation-runner.py --task schedule
```

This starts the scheduler that runs:
- Daily: Product tracking at 8 AM
- Weekly: Blog posts on Monday, Wednesday, Friday at 6 AM
- Weekly: Market insights on Sunday at 7 AM

---

## 📊 View Results

### Check Database
```bash
cd virginia-home-essentials
.venv\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('products.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM products'); print(f'Products: {cursor.fetchone()[0]}'); conn.close()"
```

### Export Blog Posts
```bash
cd virginia-home-essentials
..\.venv\Scripts\python.exe admin\export_blog_posts.py 50
```

### View Logs
```bash
type logs\automation_*.log
```

---

## 🌐 Deploy to Production

### Shared Hosting (Hostinger/Bluehost)
See [DEPLOYMENT.md](DEPLOYMENT.md) - Section 1

**Quick Steps:**
1. Upload `virginia-home-essentials/` folder via FTP
2. Set up Python environment on server
3. Add cron job: `0 8 * * * cd /path/to/project && python automation-runner.py --task full`

### VPS (DigitalOcean/AWS)
See [DEPLOYMENT.md](DEPLOYMENT.md) - Section 2

**Quick Steps:**
1. SSH into server
2. Clone repo or upload files
3. Install dependencies: `pip install -r requirements.txt`
4. Set up systemd service or cron job
5. Configure nginx

### Windows Server
See [DEPLOYMENT.md](DEPLOYMENT.md) - Section 3

**Quick Steps:**
1. Install Python on server
2. Copy project folder
3. Create Task Scheduler task to run automation

---

## 📈 Set Up Analytics

### Google Analytics 4
See [ANALYTICS.md](ANALYTICS.md) for full guide

**Quick Steps:**
1. Create GA4 account at analytics.google.com
2. Create property for your domain
3. Get Measurement ID (looks like G-XXXXXXXXXX)
4. Replace placeholder in:
   - `index.html` (line 12)
   - `blog/index.html` (line 12)
5. Wait 24 hours for data to appear

---

## 🔧 Troubleshooting

### Website won't load
```bash
# Check if server is running
python -m http.server 8000

# Try different port
python -m http.server 8080
```

### Automation fails
```bash
# Check logs
type logs\automation_*.log

# Test OpenAI API (optional)
.venv\Scripts\python.exe -c "import openai; print('API configured')"

# Check database
cd virginia-home-essentials
..\.venv\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('products.db'); print('Database OK'); conn.close()"
```

### Blog posts not showing
```bash
# Export blog posts manually
cd virginia-home-essentials
..\.venv\Scripts\python.exe admin\export_blog_posts.py 50

# Check if posts.json created
type blog\posts.json
```

### Database locked errors
- System uses WAL mode with 30-second timeout
- If still occurs, close other connections to database
- Check if automation is running multiple times

### Affiliate links not working
1. Verify tag in `.env`: `AMAZON_ASSOCIATE_TAG=virginiahomee-20`
2. Check database: `SELECT affiliate_url FROM products LIMIT 5;`
3. Test link in browser (should redirect to Amazon)

---

## 📋 Daily Workflow (Production)

### Morning Check (5 minutes)
```bash
# Check automation ran successfully
type logs\automation_*.log | findstr "ERROR"

# View latest status
type automation_status.json

# Export latest blog posts
cd virginia-home-essentials
..\.venv\Scripts\python.exe admin\export_blog_posts.py 50
```

### Weekly Review (15 minutes)
1. Review generated blog posts for quality
2. Check Google Analytics dashboard
3. Update affiliate links if needed
4. Adjust automation settings if necessary

### Monthly Tasks (1 hour)
1. Review performance metrics in GA4
2. Optimize top-performing categories
3. Update product database with new items
4. Plan next month's content calendar
5. Check and update documentation

---

## 🎯 Performance Optimization

### Speed Up Website
1. Enable HTTPS for HTTP/2
2. Compress images in `assets/` folder
3. Minify CSS/JS (optional)
4. Enable server-side caching

### Improve SEO
1. Run sitemap generator weekly:
   ```bash
   cd virginia-home-essentials
   python generate_sitemap.py yourdomain.com
   ```
2. Submit sitemap to Google Search Console
3. Monitor crawl errors
4. Build backlinks from Virginia real estate sites

### Increase Conversions
1. A/B test product descriptions (Phase 2)
2. Add social proof (reviews, testimonials)
3. Create seasonal promotions
4. Optimize mobile experience

---

## 📚 Key Files Reference

| File | Purpose | Edit? |
|------|---------|-------|
| `.env` | API keys and config | ✅ Yes |
| `index.html` | Homepage | ✅ Yes |
| `assets/script.js` | Frontend logic | ⚠️ Careful |
| `automation-runner.py` | Master automation | ⚠️ Careful |
| `blog/posts.json` | Generated posts | ❌ No (auto) |
| `products.db` | Product database | ❌ No (auto) |
| `sitemap.xml` | SEO sitemap | ❌ No (auto) |

---

## 🆘 Getting Help

### Check Documentation
- [README.md](README.md) - Full project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Hosting setup
- [ANALYTICS.md](ANALYTICS.md) - Analytics setup
- [PHASE1_COMPLETE.md](PHASE1_COMPLETE.md) - Status and roadmap

### Debug Commands
```bash
# Python version
python --version

# Installed packages
pip list

# Database info
cd virginia-home-essentials
..\.venv\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('products.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print(cursor.fetchall()); conn.close()"

# Test automation
cd ..
.venv\Scripts\python.exe automation-runner.py --task content
```

---

## ✅ Launch Checklist

Before going live:

- [ ] Update `.env` with real API keys
- [ ] Replace GA4 placeholder with real ID
- [ ] Test all affiliate links
- [ ] Generate initial blog posts (20+)
- [ ] Configure domain and DNS
- [ ] Enable HTTPS/SSL
- [ ] Submit sitemap to Google
- [ ] Test mobile responsiveness
- [ ] Monitor first week of analytics

---

**Ready to launch!** 🚀

*For detailed instructions, see the comprehensive documentation files.*

---

*Last Updated: January 10, 2026*
