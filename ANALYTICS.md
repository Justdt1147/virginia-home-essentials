# Google Analytics 4 Setup Guide

## Step 1: Create Google Analytics Account

1. Go to [analytics.google.com](https://analytics.google.com)
2. Click "Start measuring"
3. Enter Account Name: "Virginia Home Essentials"
4. Configure data sharing settings (recommended: all enabled)
5. Click "Next"

## Step 2: Create Property

1. Property Name: "Virginia Home Essentials"
2. Reporting Time Zone: "United States - Eastern"
3. Currency: "US Dollar ($)"
4. Click "Next"

## Step 3: Set Up Data Stream

1. Select "Web"
2. Website URL: `https://yourdomain.com`
3. Stream Name: "Virginia Home Essentials Website"
4. Click "Create stream"

## Step 4: Get Your Measurement ID

After creating the stream, you'll see:
- **Measurement ID**: `G-XXXXXXXXXX` (starts with G-)
- Copy this ID

## Step 5: Add ID to Your Website

Replace `G-XXXXXXXXXX` in these files with your actual Measurement ID:

### Files to Update:
1. **index.html** (line 5)
2. **blog/index.html** (line 5)

Find this code:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX', {
```

Replace **both** instances of `G-XXXXXXXXXX` with your Measurement ID.

## Step 6: Configure Enhanced Measurement

In Google Analytics:
1. Go to Admin > Data Streams > Your Stream
2. Click "Enhanced measurement"
3. Enable these (recommended):
   - ✅ Page views
   - ✅ Scrolls
   - ✅ Outbound clicks (important for affiliate links!)
   - ✅ Site search
   - ✅ File downloads
   - ✅ Video engagement

## Step 7: Set Up Custom Events

Your site automatically tracks these custom events:

### Affiliate Click Events
```javascript
gtag('event', 'affiliate_click', {
    'event_category': 'Product',
    'event_label': 'Product Name',
    'product_category': 'smart-home',
    'value': 1
});
```

### Category Selection
```javascript
gtag('event', 'category_selected', {
    'category': 'smart-home',
    'timestamp': '2026-01-10T...'
});
```

### Newsletter Signup
```javascript
gtag('event', 'newsletter_signup', {
    'email': 'user@example.com',
    'timestamp': '2026-01-10T...'
});
```

## Step 8: Create Custom Reports

### Affiliate Performance Report

1. Go to **Explore** > **Create new exploration**
2. Select **Free form**
3. Add dimensions:
   - Event name
   - Event label (product name)
   - Product category
4. Add metrics:
   - Event count
   - Total users
5. Apply filter: Event name = `affiliate_click`

### Product Category Performance

1. **Explore** > **Free form**
2. Dimensions:
   - Product category
   - Page path
3. Metrics:
   - Total users
   - Event count
   - Average engagement time

## Step 9: Link to Amazon Associates

While GA4 tracks clicks, Amazon Associates tracks conversions:

1. Log into [Amazon Associates](https://affiliate-program.amazon.com/)
2. Go to **Reports** > **Link** Performance
3. Compare GA4 click data with Amazon conversion data
4. Calculate conversion rate: (Amazon Orders / GA4 Clicks) × 100

## Step 10: Set Up Conversion Goals

In Google Analytics:
1. Go to **Admin** > **Events**
2. Mark these as conversions:
   - ✅ `affiliate_click`
   - ✅ `newsletter_signup`
3. These will appear in your conversion reports

## Monitoring & Optimization

### Daily Checks
- Real-time affiliate clicks: **Reports** > **Realtime**
- Today's conversions: **Reports** > **Engagement** > **Conversions**

### Weekly Analysis
- Top performing products (by clicks)
- Best converting categories
- Traffic sources (organic, social, direct)
- Page engagement time

### Monthly Reviews
- Conversion rate trends
- Revenue per category (from Amazon)
- SEO performance (from Search Console)
- Content performance

## Privacy & Compliance

Your site is configured for privacy:

```javascript
gtag('config', 'G-XXXXXXXXXX', {
    'send_page_view': true,
    'anonymize_ip': true  // GDPR compliance
});
```

### Required Notices

Add to your site footer or privacy page:
```
This site uses Google Analytics to analyze traffic. 
We collect anonymized data to improve user experience.
No personally identifiable information is collected without consent.
```

## Troubleshooting

### Analytics Not Working?

1. **Check if GA is loaded:**
   - Open browser console
   - Type: `typeof gtag`
   - Should return: `"function"`

2. **Verify Measurement ID:**
   - View page source
   - Search for your G-XXXXXXXXXX ID
   - Must appear in both the script URL and config

3. **Test events:**
   - Click a product link
   - Open console
   - You should see: "Event tracked: affiliate_click"

4. **Check in GA4:**
   - Go to **Realtime** view
   - Should see your current session
   - Events appear within 5-10 seconds

### No Affiliate Clicks Showing?

1. Verify Enhanced Measurement "Outbound clicks" is enabled
2. Check that product buttons call `trackAndRedirect()`
3. Ensure your affiliate tag is in URLs: `?tag=virginiahomee-20`

## Advanced: Google Tag Manager (Optional)

For more control, consider migrating to GTM:

1. Create GTM account
2. Replace GA4 code with GTM container
3. Add GA4 tag in GTM
4. Add custom triggers for affiliate clicks

Benefits:
- No code changes for new tracking
- A/B testing capabilities
- Multiple analytics platforms

---

## Quick Reference

**Your Setup:**
- Measurement ID: `G-XXXXXXXXXX` (replace this!)
- Affiliate Tag: `virginiahomee-20`
- Time Zone: US Eastern
- Currency: USD

**Key Metrics:**
- Affiliate clicks per day
- Conversion rate (Amazon / GA4)
- Top products by clicks
- Traffic sources

**Update Schedule:**
- Check daily: Realtime dashboard
- Review weekly: Conversion reports
- Analyze monthly: Full performance report

---

**Setup Complete! 🎯**

Your Virginia Home Essentials site now has full analytics tracking for affiliate performance optimization.
