# Deployment Guide - Virginia Home Essentials

## Prerequisites

- Python 3.8+ installed on your hosting server
- Domain name pointed to your hosting provider
- SSH/FTP access to your web server
- Amazon Associates account activated
- (Optional) OpenAI API key for AI content generation

## Quick Deployment Checklist

- [ ] Upload files to web server
- [ ] Set up Python virtual environment
- [ ] Configure environment variables (.env file)
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Initialize databases (`python admin/automation-runner.py --task full`)
- [ ] Set up scheduled automation (cron or Task Scheduler)
- [ ] Configure domain SSL certificate
- [ ] Test affiliate links
- [ ] Submit sitemap to Google Search Console

---

## Deployment Options

### Option 1: Shared Hosting (Recommended for Beginners)

**Recommended Providers:**
- **Hostinger** ($2-$4/month) - Best value, Python support
- **Bluehost** ($3-$8/month) - WordPress-friendly, easy setup
- **SiteGround** ($3-$15/month) - Great performance

**Steps:**

1. **Upload Files via FTP**
   ```
   Upload entire virginia-home-essentials folder to public_html/
   ```

2. **Access via SSH** (or use hosting control panel)
   ```bash
   ssh username@yourhost.com
   cd public_html/virginia-home-essentials
   ```

3. **Set up Python Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cd admin
   cp .env.example .env
   nano .env  # Edit with your API keys
   ```

6. **Initialize System**
   ```bash
   python automation-runner.py --task full
   ```

7. **Set Up Cron Job** (Automation)
   - Open cPanel > Cron Jobs
   - Add daily job:
   ```
   0 2 * * * cd /home/username/public_html/virginia-home-essentials/admin && /home/username/public_html/virginia-home-essentials/venv/bin/python automation-runner.py --task full
   ```

---

### Option 2: VPS/Cloud Hosting (Recommended for Scale)

**Recommended Providers:**
- **DigitalOcean** ($6-$12/month) - Developer-friendly
- **AWS Lightsail** ($5-$10/month) - Amazon ecosystem
- **Linode** ($5-$10/month) - Simple pricing

**Steps:**

1. **Create Droplet/Instance**
   - Ubuntu 22.04 LTS
   - Minimum: 1GB RAM, 25GB SSD

2. **Connect via SSH**
   ```bash
   ssh root@your-server-ip
   ```

3. **Update System**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y
   ```

4. **Create Non-Root User**
   ```bash
   adduser virginia
   usermod -aG sudo virginia
   su - virginia
   ```

5. **Upload Project**
   ```bash
   cd /home/virginia
   # Option A: Use git
   git clone your-repo-url virginia-home-essentials
   
   # Option B: Use SCP from your local machine
   scp -r /path/to/virginia-home-essentials virginia@your-server-ip:/home/virginia/
   ```

6. **Set Up Virtual Environment**
   ```bash
   cd virginia-home-essentials
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Configure Environment**
   ```bash
   cd admin
   cp .env.example .env
   nano .env  # Add your API keys
   ```

8. **Initialize System**
   ```bash
   python automation-runner.py --task full
   ```

9. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/virginia-home-essentials
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       root /home/virginia/virginia-home-essentials;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }

       location /admin {
           deny all;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/virginia-home-essentials /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Set Up SSL (Free with Let's Encrypt)**
    ```bash
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

11. **Set Up Cron Job**
    ```bash
    crontab -e
    ```

    Add:
    ```
    # Run automation daily at 2 AM
    0 2 * * * cd /home/virginia/virginia-home-essentials/admin && /home/virginia/virginia-home-essentials/venv/bin/python automation-runner.py --task full >> /home/virginia/logs/automation.log 2>&1
    ```

---

### Option 3: Windows Server (Local or Cloud)

**Steps:**

1. **Install Python 3.8+**
   - Download from python.org
   - Add to PATH during installation

2. **Extract Project**
   ```
   Extract virginia-home-essentials.zip to C:\inetpub\wwwroot\
   ```

3. **Open PowerShell as Administrator**
   ```powershell
   cd C:\inetpub\wwwroot\virginia-home-essentials
   ```

4. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

5. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Configure Environment**
   ```powershell
   cd admin
   copy .env.example .env
   notepad .env  # Edit with your keys
   ```

7. **Initialize System**
   ```powershell
   python automation-runner.py --task full
   ```

8. **Set Up Task Scheduler**
   - Open Task Scheduler
   - Create Basic Task
   - **Name:** Virginia Home Automation
   - **Trigger:** Daily at 2:00 AM
   - **Action:** Start a program
   - **Program:** `C:\inetpub\wwwroot\virginia-home-essentials\venv\Scripts\python.exe`
   - **Arguments:** `automation-runner.py --task full`
   - **Start in:** `C:\inetpub\wwwroot\virginia-home-essentials\admin`

9. **Configure IIS** (if using Windows Server)
   - Open IIS Manager
   - Add new website pointing to virginia-home-essentials folder
   - Bind domain name
   - Restrict /admin folder in IIS

---

## Post-Deployment Configuration

### 1. Verify Automation is Working

```bash
# Check logs
tail -f admin/logs/automation_*.log

# Manually run a test
cd admin
python automation-runner.py --task products
```

### 2. Test Affiliate Links

- Open your site in browser
- Click on several product links
- Verify they redirect to Amazon with your affiliate tag
- Check format: `amazon.com/dp/[ASIN]?tag=virginiahomee-20`

### 3. Set Up Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add your property (yourdomain.com)
3. Verify ownership (HTML file upload or DNS)
4. Submit sitemap: `https://yourdomain.com/sitemap.xml`

### 4. Configure Analytics

See separate guide for Google Analytics integration (Step 6 in main plan)

### 5. Monitor Performance

**Check Daily:**
- Automation logs for errors
- Affiliate link clicks (Amazon Associates dashboard)
- Site uptime

**Check Weekly:**
- Google Search Console for SEO performance
- Product database freshness
- Blog post publication

---

## Troubleshooting

### Automation Not Running

```bash
# Check if cron job is set
crontab -l

# Check Python path
which python3

# Test manually
cd admin && python automation-runner.py --task content
```

### Database Locked Errors

- Already fixed with WAL mode
- If issues persist, check file permissions:
```bash
chmod 644 admin/*.db
```

### Missing Products

- Check Amazon Associates account is approved
- Verify AMAZON_ASSOCIATE_TAG in .env
- Run: `python admin/automation-runner.py --task products`

### OpenAI API Errors

- Verify OPENAI_API_KEY in .env
- Check API quota at platform.openai.com
- System works without OpenAI (uses fallback content)

---

## Security Checklist

- [ ] `.env` file is NOT publicly accessible
- [ ] `/admin` folder is password-protected or blocked
- [ ] SSL certificate is active (HTTPS)
- [ ] Database files (*.db) are not in public folder
- [ ] automation_config.json doesn't contain real API keys
- [ ] Regular backups configured
- [ ] Server firewall is enabled

---

## Backup Strategy

### Automated Daily Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/home/virginia/backups"
PROJECT_DIR="/home/virginia/virginia-home-essentials"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/backup-$DATE.tar.gz $PROJECT_DIR/admin/*.db $PROJECT_DIR/admin/*.json

# Keep only last 7 days
find $BACKUP_DIR -name "backup-*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```
0 3 * * * /home/virginia/backup.sh
```

---

## Performance Optimization

### Enable Caching

Add to Nginx config:
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Enable Gzip Compression

Add to Nginx config:
```nginx
gzip on;
gzip_types text/css application/javascript text/html application/json;
gzip_min_length 1000;
```

---

## Scaling for Growth

### When to Upgrade

- **> 10K visitors/month:** Upgrade to VPS
- **> 100K visitors/month:** Add CDN (Cloudflare)
- **> 500 products:** Optimize database indexes
- **> 100 blog posts/month:** Consider separate blog database

---

## Support

For technical issues:
1. Check logs: `admin/logs/automation_*.log`
2. Review troubleshooting section above
3. Check individual Python files for documentation

---

**Deployment Complete! 🚀**

Your Virginia Home Essentials site should now be live and generating automated content.
