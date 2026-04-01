# Facebook Property Listings API

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 7/28/2025 15:48:17  
**Updated:** 11/5/2025 1:04:09  
**Exported:** 3/19/2026 17:05:39  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/0b406d75-c3f4-8322-8e6c-c6700cdd49c6](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/0b406d75-c3f4-8322-8e6c-c6700cdd49c6)  

## Prompt:
what are the data fields available via api from facebook for property listings

## Response:
Facebook does not have a public, dedicated API specifically for real estate or property listings. However, you can access some property-related data through a combination of the following APIs **if** the listings are published via Facebook Marketplace or Facebook Pages using catalogs and structured listings.

### 1\. **Facebook Marketplace (limited access)**

There is **no official public API** for Facebook Marketplace. Access is **restricted** and typically reserved for large partners through **Facebook’s Commerce or Marketplace Partner Program**.

If approved, the data available includes:

*   `listing_id`
*   `title` (e.g. "3BR Condo in Miami Beach")
*   `description`
*   `price`
*   `currency`
*   `location` (latitude, longitude, or city name)
*   `property_type` (e.g. apartment, condo, house)
*   `number_of_bedrooms`
*   `number_of_bathrooms`
*   `square_footage`
*   `year_built`
*   `listing_status` (available/sold)
*   `listing_url`
*   `photos` (array of image URLs)
*   `date_posted`
*   `seller_id` / `page_id`
*   `contact_info` (may include masked or redirected details via Messenger)

> 🔒 Access to these fields requires being an approved Marketplace Partner.

* * *

### 2\. **Facebook Catalog API (for property catalogs via Business Manager)**

Used for real estate businesses uploading property listings as a **product catalog** (structured data feed).

Relevant fields (via **Marketing API > Product Catalogs**) include:

*   `name` (property title)
*   `description`
*   `availability` (`available_for_rent`, `available_for_sale`)
*   `price`, `currency`
*   `address`:
    *   `street_address`
    *   `city`
    *   `region`
    *   `country`
    *   `postal_code`
*   `latitude`, `longitude`
*   `property_type` (`apartment`, `condo`, `house`, etc.)
*   `image_link` (main photo)
*   `additional_image_links`
*   `listing_id` or `retailer_id`
*   `year_built`
*   `number_of_bedrooms`
*   `number_of_bathrooms`
*   `square_footage`
*   `listing_type` (`new`, `resale`, etc.)
*   `url` (link to full listing)
*   `neighborhood`
*   `agent_name`
*   `agent_phone`
*   `agent_email`

These are uploaded as a **feed** or added via API using:

```
POST /{catalog-id}/products
```

* * *

### 3\. **Graph API (Facebook Pages or Business Manager)**

If listings are posted manually to Facebook Pages, you can **scrape structured data** by accessing public posts or Page metadata. Example fields (non-catalog-based):

*   `message` (may include property description, price, etc.)
*   `created_time`
*   `attachments` → image and video
*   `permalink_url`
*   `location` (if tagged)
*   `from` (Page info)

Limitations:

*   **No structured property fields** (e.g. bedrooms, sqft)
*   Limited to what the post content manually includes
*   Rate limits and privacy restrictions apply

* * *

### Summary Table

| Source | Access Level | Structured Fields Available | Use Case |
| --- | --- | --- | --- |
| Facebook Marketplace API | Partner only | ✅ Full listing fields (price, beds, etc.) | Large marketplaces & integrations |
| Product Catalogs (Real Estate) | Business accounts | ✅ Structured data for real estate ads | Real estate firms using ad catalogs |
| Graph API (Page posts) | Public w/ token | ❌ Unstructured posts (message, image, time) | Scraping public listings |

* * *

If you're building a system to aggregate property listings from Facebook, your **best approach** is:

1.  **Use Real Estate Catalogs** if you’re a verified business.
2.  **Apply to Facebook’s Marketplace Partner Program**.
3.  **Scrape public Page posts** (if listings are informal or manually posted).
4.  Combine this with **external CRMs or listing feeds** (Zillow, MLS, etc.) for structured data enrichment.

Would you like sample API requests or a Google Sheet version of all the fields listed above?

## Prompt:
create a list of everything required to automatically scrape as much public data about properties listed within a geographic area as cost effectively as possible

## Response:
To automatically scrape as much public data about **properties listed within a geographic area** as cost-effectively as possible, you’ll need a system that combines **geospatial targeting**, **web scraping**, and **data enrichment** via APIs. Here's a complete list of everything required—divided into **Tools & Infrastructure**, **Data Sources**, **Scraping Logic**, **Data Storage**, **Compliance**, and **Optimization**.

* * *

✅ 1. TOOLS & INFRASTRUCTURE
---------------------------

### 💻 Core Technologies

*   **Python** or **Node.js** (for scripting and automation)
*   **Scrapy**, **Playwright**, or **Puppeteer** (headless browser automation for complex sites)
*   **Geocoding API** (e.g., Google Maps, OpenCage) to convert areas to coordinates
*   **Proxy service** (e.g., BrightData, Smartproxy) to avoid IP blocks
*   **Scheduler** (e.g., cron jobs, Airflow) to run scraping jobs regularly
*   **Docker** (optional, for containerization and deployment)

* * *

🌐 2. DATA SOURCES
------------------

### 🏠 Real Estate Platforms (Scrapable)

| Platform | Notes |
| --- | --- |
| Realtor.ca (Canada) | Moderate protection, fields like price, sqft, photos |
| Zillow | US-based, has anti-bot detection |
| Redfin | Easier than Zillow, includes sold data |
| Facebook (Pages) | Use Graph API or public post scraping |
| Craigslist | Very simple HTML structure |
| Kijiji | Canadian classified site |
| Local MLS sites | Depends on your target market |

### 📊 Supplementary APIs for Enrichment

*   **Google Places API** (business and area enrichment)
*   **Google Maps Geocoding API** (lat/lng from location text)
*   **OpenStreetMap / Nominatim** (free geocoding alternative)
*   **GeoNames** (timezone, altitude, postal code info)
*   **Zillow API (unofficial)** or private MLS data for historical sale data

* * *

🧠 3. SCRAPING LOGIC & TARGETING
--------------------------------

### 🎯 Geographic Targeting Strategy

*   Use **bounding boxes** (lat/lng rectangles) to define the region
*   Optionally convert cities or postal codes using a **geocoder**

### 🧱 Scraping Fields to Capture (Where Available)

| Category | Fields |
| --- | --- |
| Listing Info | Title, price, description, listing URL, date posted |
| Property Details | Property type, bedrooms, bathrooms, square footage, lot size, year built |
| Media | Main image URL, photo gallery URLs |
| Seller Info | Name, phone (if public), listing agency, contact method |
| Address | Street, city, state/province, postal code, country, latitude, longitude |

* * *

💾 4. DATA STORAGE & PIPELINE
-----------------------------

### 📥 Capture and Save to:

*   **PostgreSQL** with PostGIS (for spatial queries)
*   **MongoDB** (flexible schema for variable data sources)
*   **Google Sheets** (for quick viewing)
*   **S3 / GCP Buckets** (for storing raw JSON or HTML)

### 🛠️ Data Pipeline Options

*   Use **Apache Airflow** or **Prefect** for orchestration
*   Trigger pipelines with **event-based triggers** or time intervals

* * *

🔐 5. LEGAL & COMPLIANCE (Important)
------------------------------------

*   **Check each site’s Terms of Use**: Some prohibit scraping (e.g., Zillow)
*   **Avoid logging into user accounts** unless permitted
*   **Respect robots.txt** (unless legally cleared)
*   Use **ethical scraping** practices (throttle requests, rotate IPs)
*   Store only **public** data—**no PII unless explicitly visible and legal**

* * *

💡 6. COST OPTIMIZATION STRATEGIES
----------------------------------

| Component | Free Option | Paid Option (Scalable) |
| --- | --- | --- |
| Geocoding | OpenStreetMap | Google Maps API ($0.005 per call) |
| IP Rotation | Free proxies / Tor | BrightData, Oxylabs |
| Scraping Engine | Scrapy/Playwright (free) | Zyte (Scraping-as-a-Service) |
| Hosting | Local machine / free-tier cloud | GCP / AWS / Azure |
| Storage | Google Sheets / SQLite | PostgreSQL on managed cloud |
| Worker Execution | GitHub Actions / cron | Cloud Functions / Docker containers |

* * *

🧩 OPTIONAL ENHANCEMENTS
------------------------

*   📈 **Automated Property Valuation Model** (AVM) using regression on scraped comps
*   🧭 **Map visualization** using Leaflet.js or Mapbox
*   🧑‍💼 **Lead extraction**: parse emails/phone numbers of listing agents
*   🔍 **Sentiment analysis** on listing descriptions
*   🎯 **NLP-powered property matcher** (for investor profiles)

* * *

✅ Final Checklist (Summary)
---------------------------

| Item | Status |
| --- | --- |
| \[ \] Scraper logic with geolocation targeting |  |
| \[ \] Proxy rotation and throttling logic |  |
| \[ \] Real estate site field mapping |  |
| \[ \] Geocoding pipeline |  |
| \[ \] API integration for data enrichment |  |
| \[ \] Database or Google Sheets pipeline |  |
| \[ \] Scheduler for repeat scraping |  |
| \[ \] Legal review & rate-limit respect |  |
| \[ \] Cost tracking of proxies & APIs |  |

* * *

Would you like a ClickUp-compatible task list or a Google Sheets version of this breakdown with API links and sample payloads?

## Prompt:
create a clickup task checklist to complete all optional enhancements of a scraper set to automatically capture new listings every 24 hours with contact information so that they can automatically be contacted

## Response:
Here is a **ClickUp-compatible task checklist** to implement **all optional enhancements** for a property listing scraper that captures **new listings every 24 hours** and extracts **contact info for automatic outreach**.

* * *

### 📂 Folder: **Real Estate Scraper Automation**

#### 📁 List: **Optional Enhancements – Daily Property Scraper with Outreach**

* * *

### ✅ PHASE 1: Property Data Capture Automation (Baseline)

#### Task Group: 📍 **Daily New Listing Capture**

*    Build geofenced scraper to capture listings posted in the last 24h
*    Add date filtering logic to exclude previously seen records
*    Set up scheduled scraping using cron, GitHub Actions, or Airflow
*    Enable automatic IP rotation and user-agent spoofing
*    Log successful and failed scrapes by timestamp and source

* * *

### ✅ PHASE 2: Contact Extraction & Normalization

#### Task Group: 🧑‍💼 **Contact Details Parsing**

*    Extract name, phone number, and email from listing metadata or description
*    Use regex + NLP for fuzzy extraction from free-text
*    Normalize phone formats (E.164 international standard)
*    Validate and deduplicate contact entries
*    Tag entries with contact source confidence level (e.g. "high", "partial", "scraped")

* * *

### ✅ PHASE 3: Outreach System Integration

#### Task Group: ✉️ **Automated Contact Engine**

*    Set up outbound email automation via SendGrid, Mailgun, or Gmail API
*    Set up SMS messaging via Twilio or MessageBird
*    Configure webhook payloads for CRM (e.g., HubSpot, Close, GoHighLevel)
*    Create message templates per contact method (email/SMS)
*    Add opt-out logic to comply with spam regulations

* * *

### ✅ PHASE 4: Enrichment & Intelligence

#### Task Group: 🧠 **Intelligent Enhancements**

*    Build basic Property Valuation Model (AVM) using scraped comps
*    Extract keywords and sentiment from property descriptions
*    Tag listings by property type, condition, urgency
*    Rank properties based on price/sqft and time-on-market
*    Score leads using NLP profile matching (investor vs retail)

* * *

### ✅ PHASE 5: Visualization & UI

#### Task Group: 🗺️ **Map & Dashboard Integration**

*    Set up real-time map view with Leaflet.js or Mapbox
*    Color-code properties by price percentile or opportunity score
*    Create Google Sheets export with formatted contact columns
*    Build admin dashboard for listing pipeline view

* * *

### ✅ PHASE 6: Data Pipeline & Storage

#### Task Group: 💾 **Persistence & Sync**

*    Push new data to MongoDB or PostgreSQL (PostGIS if spatial search needed)
*    Back up listings and contact info to cloud storage (GCP, S3)
*    Maintain versioning of records to track listing changes over time
*    Sync enriched data to CRM or outreach tool every 24h

* * *

### ✅ PHASE 7: Compliance & Error Handling

#### Task Group: ⚖️ **Legal, Ethics, and Redundancy**

*    Add robots.txt compliance checks and domain-specific throttling
*    Validate all contact info against opt-out or Do Not Call registries
*    Implement retry queue and failed job logger
*    Auto-email error logs for failed scrapes or missing contact data

* * *

### Optional Tags:

*   `#automation`
*   `#real-estate`
*   `#outreach`
*   `#AI`
*   `#data-pipeline`
*   `#clickup-integration-ready`

* * *

Would you like me to export this into a CSV or ClickUp importable format directly? I can also generate a Google Sheets tracker for the same.

## Prompt:
clickup importable format

## Response:
Here is your ClickUp-importable task list for the enhanced real estate scraper project:

📥 Download ClickUp\_Importable\_RealEstate\_Scraper.zip

You can import this directly into ClickUp under a list or folder to begin execution. Let me know if you'd like a version with due dates, assignees, or subtasks preconfigured.

## Prompt:
how

## Response:
Here’s a **step-by-step guide to import this CSV task list into ClickUp** so you can use it as a fully functional project board:

* * *

✅ **HOW TO IMPORT INTO CLICKUP**
--------------------------------

### 🔄 **Option 1: CSV Import (for a new list)**

1.  **Unzip** the downloaded file  
    Extract `ClickUp_Importable_RealEstate_Scraper.csv` from the ZIP archive.
2.  **Log into ClickUp**
3.  Go to the **Workspace** or **Folder** where you want to import the tasks
4.  Click the **\+ New List** button
5.  Choose **“Import”** (instead of creating a blank list)
6.  Select **CSV**
7.  Upload the `ClickUp_Importable_RealEstate_Scraper.csv` file
8.  In the import wizard:
    *   **Map “Task Name”** to `Task Name`
    *   **Map “Task Content”** to `Description` (or custom field if preferred)
    *   **Map “Tags”** to `Tags`
9.  Complete the import — ClickUp will auto-create the list and tag each task accordingly.

* * *

🛠 **Customizations After Import**
----------------------------------

After importing, you can:

*   Group tasks by `Task Content` (this acts like your "Phase")
*   Add custom fields like:
    *   **Assignee**
    *   **Due Date**
    *   **Status**
    *   **Priority**
*   Create **automations** (e.g., notify when status is changed)
*   Apply **filters** for tags like `#automation`, `#outreach`, etc.

* * *

Would you like me to add **due dates, assignees, subtasks**, or a **ready-made ClickUp Board layout export** next?

## Prompt:
can you export this as a csv

## Response:
Here is the CSV file for your ClickUp import:

📄 Download ClickUp\_Importable\_RealEstate\_Scraper.csv

You can upload this directly into ClickUp using the CSV import option as described earlier. Let me know if you want it pre-filled with due dates, priorities, or task dependencies.

## Prompt:
create a google sheet with all data fields able to legally be captured automatically broken down into tabs for each category of data and labeled with any requirements needed to access it, ex: developer account, publicly shared, registered business account

## Response:
Your Google Sheets-compatible Excel file is ready:

📄

Property\_Data\_Fields\_Legal\_Access.xlsx

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmYAAAEsCAYAAABpB38dAAAQAElEQVR4AeydCbyV0/7/v89xUVTKL6S6mgwpVxn/SShCMpTMEmXKNbsZIwpJXFQqw6VJZg1XoZupULekAZVukVIS3dItrnCr/36v3To9Z5+9z7jPOXv4eLWeYU3PWu/nqf3xXd+1Vs6aNWu2pnJYsWJFSrevPNiJQfQbFQdxCP990/eg70HfQ/QbEIfM4pBjkf922WUXS8UQaZr7k4ptK882OQiRQ3k+MxWfFUHg/qRi28qzTQ5C5FCez0zFZ0UQuD+p2LbybJODEDmU5zOL96zy+X2JIHB/UrFt5dkmByFyKM9npuKzIgjcn1RsW2FtcsLMtV4HERABERABERABERCBCiUgYVah+PXwdCSgNouACIiACIhAWRGQMCsrsqo3Iwls2LDBli9fbr/88ktG9k+dEgERKBmBLVu22OrVq+0///lPySpQKRHYRiDHbNuVTnEJdOvWzdq1a2e///573PRMjkSAHHvssRYOF198sX300UeZ3O24fVu2bJldfvnldtppp1mXLl3s5JNPtkGDBtn//ve/uPkzMfKDDz7I8y3w9+Lmm2+2JUuWZGJ3E/bp119/zcMh/Pfj/fffT1guExOuueaauCxmzJiRid2N26etW7faG2+8Ye3bt7dzzz3XTj/9dDv//PPtvffei5s/UyPpL/8mxPavZ8+eNnjw4NjorLh/+OGHrW/fvsXuqyxmBSD76quvjPDf//7XZs2aVUDOzEziHxx69uKLL9qbb75pr732mh144IHGX7RNmzaRlBWB/wO+6qqrrGnTpvbWW28ZP75Dhw51TEaOHJkVDMKd/Pvf/26EXr162Y477miXXXaZLVu2LJwlo6/93wv+wX355ZctHI466qiM7nu8zp133nl5GMCjefPmebNm8N3bb79t/fv3t7vuusv92zBx4kQnznr37m2LFi3K4J7n7Zr/e5E3NrvvsKKWhIuEWQHfzTvvvGMnnHCCs5jxl6+ArBmdtOuuu1qVKlVszz33tKOPPtr1NZssRePHjzcYXHfdde68ww472EEHHeT+Id55550dj2w61KhRwwh8C/369XOClR/jbGJAX/fYYw/be++984RKlSqRlFVht912y8MAJtnEYciQIcb/uLVq1cr4t6FatWp24YUX2iWXXGL//ve/s+pbUGeTQ0DCLAHHzZs3O4tI27ZtrU2bNvbuu+/azz//nCB3ZkcjSrGYvfDCC4alCFM9Qi2ze729d0uXLrXDDz/c/vCHP/hId+Yf4osuushdZ/PhyCOPdJblbGPAcB3/8+YD/0ZkGwP6y1C2Z8B57ty5RGdF+PHHH43Avw++w7i98D+uuH1kmwWV0aXnn3/ewgGXGM9G56IRkDBLwIl/XPAl4Ufn0EMPdbmmT5/uztl2mDZtmk2ZMsXo//r16+3bb7812GQLh40bNzpLWbb0t7j9xGKSTUPbns+kSZPspZdeyg3ZaDWExcyZM2348OG5AV8j4rMheIsYFnX6y7+NjLL40KNHD6KzKnz66acWDmvXrs2q/iejs1FhloyaMqyOf/zjH4b6x9EbkzTdw3LEOdtC79697aGHHnIOnPz4fP311/bxxx9nDYY6deoYQj22w/hVjRs3LjY66+5XrVplBxxwQNb1u3fk78UzzzxjPjz99NNZx4AOYzUOW0iySYz83//9Hwhyfclq1apl+OQSzjzzTJeWTQcWTuW3Ihy8YSObOJS2rxJmcQgiyBBmN954o916660ucM3QBWbrOEWyJgrrCL41iLNs6XTDhg3dUF3su+cfXyaHZAuHeP3Ecsr/sGSjMIvHQ3GJCWRiCr6WiBH/P274mPE/cgQN4WXiGy+fPkmYxeHMchD8ZTvjjDMMtU/Ar4q4qVOnximR2VErV660b775xr744gt77LHHbPHixdaiRYvM7nSod6eccoohRh988EH77rvvjGE7psczQ5NvJJQ1Ky75Fgiff/65/eUvf7HKlStbu3btsqLv4U7CAGEeDszgDefRdWYTCILAunfvbq+//roxW5v/UeF/Wh9//HGbM2dOZndevSszAhJmcdBOnjzZ/dCEnb1ZFoBJAFgH4hTJyKggCFy/rr76amO4gn+A+D9DlsvYf//9XVo2HJhhxtIICFSWBjjppJOsf//+zpKaTRz8u+ZbINxyyy1Wu3ZtN8ydTZNBgiD69+L++++3bt265QnZ5F/lv4dsP/M/7fx9uOeee+zEE090szEXLlzoZm3n5ORkDZ4giP69yJoOF6GjJX3/2fPVFAGiz/LXv/7VbowMY/p7f77tttuMqdH+PtPP9erVMxYVDYdRo0Y50ZrpfY/tX+PGjW306NE2ZswYY3Yq/3fMYrOx+TL5noVUw98Czu933nmn7bPPPpnc7Xx9Y4mUMIfwdbb5FfHvIaIkH6QsiuB/4K+88krjf+hZ1xBL+hNPPGH8D9yjjz6aNSSOP/5449+E2A4/8MADdu2118ZGZ8U9//PK+nbF7WyuMCtuQeUXgWwjEASBG9KsW7euW68o2/qv/oqACCQmgGW9QYMGmsGdGJFSikhAwqyIoJRNBERABESgVARUWAREoAgEJMyKAElZREAEREAEREAERKA8CEiYlQdlPSMzCahXIiACIiACIpBkAk6YsW5XKgb6ytYWqdi28mwTHAjl+cxUfBYMCKnYtvJsEwwI5fnMVHwWDAip2LbybBMMCOX5zFR8FgwIqdi28mwTDAjl+cxUfBYMCKnYtsLalMOaTNuCW58p1a7Hjh2bu+VJePuTbLq+9957jSUqsqnP8fr6t7/9zViOYMuWLZbtgb/Y2c6Af6tYN0wcNpk4bHG/X+IgDv7fg3T+9yGHmSS77767pWKgbTvttJObast022wNbBJMyNb++36zJgyL3O65556WzYHlKQjZzIC+77XXXln9HcCAkF4cyu7vrjhE2YpD+nNwQ5mY+xREQAREQAREQAREQAQqloCE2Tb+LA44ceLEbXeJT2vXrnWLzL766qtxM7GfIosustl33AyKLDcC//73v23YsGHGJttl9VDVKwIiIAIiIALJJJBVwqxPnz7WuXPnPIEVm1esWGEnn3yysbUG+/8VBHj16tVuaDXRis4//PCDS3/kkUcKqiYpabSB/iA+klJhGVTSv3//XN4XX3yx9e7d29iupAwela/KXr162WWXXRZ3F4d8mVMgYvr06XFXzk6BpqkJIiACIiAC5UQgRpiV7qlYi2699VbnhFm6msqm9BtvvOG202FLHR9wMv+///s/O/TQQ419D+vUqVM2D09yrT/99JP16NHD9eeOO+4wZq8m+RFJqW7q1KmujfB+7rnnrE9EHDdt2tSKYp0sbQNatmxpVatWNbYSKm1d5VGefRfZvqQ8nqVniIAIiIAIpCaBpAgzZj8wFHjffffZjBkzbPPmzanZ222tmjZtmm3dutWFDRs22C677GKDBg2yp556ynbbbbdtucwWLFhg48aNK7RPv//+u9tTkuHNb7/9Nrd8WV5MmDAht3qsdAig3IhtFzjKs7fjJ5984mYxbou2RPHr16+3d99914mm2OE/yrz22msu/bfffvNVubrixedm2Hbx5ptvupljCHeiHnvsMU4uUN/MmTMda57jIkOHTz/91J5//nn77rvvjDZOmTLFCdGlS5ca18STnZmK3NNf7tm77fXXX7dTTjnFfZOkffPNN/b9998bbeZ/JMhHnfH6DYOPPvrIqBdrFsL+559/diz5hnjf//rXv6giT4j33SCkeT4W12XLlhll+btCQf6+0MfFixc7RrTff0f0jT7wvn17KaMgAmlLQA0XAREokEBShBk/OvxQFfikFE/kx7tNmzb266+/GkLhvPPOs4MOOsg6depkRx11lB133HHuBzq2G/T9hBNOcOnnnnuucR2bpyzuR44c6aodPXp0nrO7iRyuueYaa9KkiZ199tl2xBFH2BlnnGH8lyieZSiY6de2bVs3pIvlEPFAmb/+9a+urnPOOcdIh0dB8aTFC9WqVbPzzz/fJeH/xQVCifa1aNHCsabNWAJJI3DdvHlzu+iii5xwHjBggPGe4P7000+767feeousxpA0aVdffbW7xyrHPax4r1yfeOKJdvDBBxt9QQwV1O9JkybZMcccYwcccIAdffTRdtpppznrG31o1aqV8b4bN27slnPhgQV9N19//bVrK31lPz3KwvEvf/mLG9qlj9Tx2Wefuff17LPPOrFfu3Zt69Chg3t/9erVk78ckBREQAREIIMJJEWY1axZ0w1RsaxBOrDC+oLYIMSzeOC8/8orrziBwg8lw0sIz8GDB+fr3tChQ+3DDz90P+Dz5s0z1hzLlynJEVhT/vGPf7jh1wsuuMAtGTBixAhDrPAoBAXtatiwodHuJ5980hCaieI3btxo1MMZMYZgoSz+WViLfJ/mzJljWG/uv/9+HpPb19h4lxhzWLlypWEJuueee1zKqaee6s58MzC+6667bNGiRXbmmWcavnNYkwhcsyTAlIiVDEHkCpXigFUKoYX/GUK0oH77xyAo4d2lSxejrzDC4ratL4almLxF+W7g8Mwzz9iLL75IEcNyiPjyAhvR+PHHHxu+j/57Q6T985//NL5X8rqCOoiACIiACGQkgaQIs3Qjg2i55ZZbjMCwU2z7ER/E/eEPfzAE2po1a7h1Q5ruInTgB5vbu+++25o1a+asKNyXZaBN1I/VhbW9LrzwQm6N4S4u3nnnHU6GNQY/q+7duxuiIlE8YoPhUPyxEGUIj+rVqxtC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4J133mmvv/66IXAGDRpUhBIlz8KQ3oQJE1wF9evXd2ccx6+66ir78ssvzYsVlxA5LFy40K699lonHNmuAjGH8MBSxo82YgzrzHfffefKXnHFFZFSqf8nHofCWo1YQ7j+9NNPhpBDxCBOCyqHDyHCm4kd8JszZ44TwOEy3bp1c7djx45150WLFtmsWbPs8ssvd/f+gHUTf65XX33VWT7nz59viCqfXrlyZSMPEw/2339/985IC4LAjjvuOJeGlbR169Z29913k+QC+XmfS5YscZbUnj172kcffWTcr1ixwkaPHm28c+rGWse3QsBqxrtHrLuKdBABERABERCBCiKQFGGGH5K3MFWvXt34wfTDSsnuF9aUjh07Gj/YCAXCzjvv7B5DHEOXjRo1Mn7cXeS2w+TJk90VQoQLLCQtW7a0xYsXu8D9a6+9Zs8884wri6CIHf6jXKqEgjgU1kYc/Jmoseuuu1r37t1ddvrrLhIcEMFYyo455hiX45BDDrGGDRu6a3/g/pRTTrFhw4a5qJdeesnl8WVcZOSARTVyMiyYU6ZMMSx6Po54BB6WMoagO3ToYAwxE1+7dm0nxEjj/bZp08YQf6T5MHDgQGeJw+KGdaxp06b23nvvGRMe/JApIvTdd991RW644QZnRSU/FkQXqYMIiECFENBDRUAEzJIizOrXr2/8COOngzWCWZAMIZUFYIalGMbCtwyrx8UXX5z7mL322iv3OvYCq8iee+5pXsT5dOK5rlKlivNR4558LPuBAzxpqRgK4lCc9jI0SX4sUJwTBd6tz5soD/GIdIYlsVo+++yzdt1111kQBCTlBgQhwgi/MMQVFtbl25boyM207YK82y7dTNEHHnjAGHbm3TA5IbbdfggdyxlpDFXyTglY+hhqR0DSH+qlLs4KIiACIiACIpAKBJIizM4880xjqPDcc8+1s846y7BoxA4lJquzOKPjE8WQFD+wRa0XawtDXTj/h8v4OhAIt99+u/lw66232k477RTOmlLXiTggPMNO8YU12lvKENcF5W3QoIEtWLCgoCwuDYsZwrZr167Otw+fL5cQczj++OON2bzz5s0zho9HjRoVkyP/LZNMsIhhJWUIF6th/lzRGIQb7xbrqX+n/kxfvIhHrEVLmDFRwl8n56xaREAEREAERKB4BJIizBhCZBgQHx5mZWLN8j98xWtO2eVG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cA2Xia2vuPcIebaSYneC4pZNRn62x2Lv1WTUpTpEQATKmICqF4EMJZAUYYYoYhsdAlv/LFmyxPr161fqlfTDzNlG6aGHHjLETTge8cfWPOyjGI6PvR45cqSxL6aPb9Omjd14443G2ccl43z77bcb2wMhbBYsWGCIv9mzZ7uq2QqJPTTdTSEHRMrFF19sbC8VzopVCQ7Tpk2z9evX25NPPmnsv9m7d+9wtlJfF5VrqR+kCkRABERABERABHIJJEWY5dYWucCCw56UWNEit+Xy59JLL7VTTz0191lY7GbMmGGrVq3KjVu8eLEbtkTgEdhX84EHHjA2HScTw2eIIfbLREgxjEd8OCA4EUQsxhuO99eIMfr/2GOP2bPPPmsTJ0409u5k03TysL8keXg+libiWHOGfR+plz0giSP455OXQFw4dOnSxRhCZq/Lrl27GntssrggfaYvPi8WPJ5L33wc599++80NafrnEBcbYrmSTv0zZ8409vHkPhxIYxP4cBysli5dGo7Kvabt1MXeoLmR2y6on3cYK0wT8WLHAd9vrLXhfsGXuqhzW/W5J9qHxXH16tW5cRV0oceKgAiIgAiIgCVVmGEhQmBceOGF5YoWC1WvXr3cM1966SVDdHXu3Nnq1Kljjz76qB155JE2YcIEZ12KXa9t/vz5rhzCjnbvsccedvjhhxvDeIgsEhEDWK/2339/Y6iPvRr32msvS2SlQwRShrIHHHCABUFgRx11lNE2LHe04e677zZETNu2ba1evXrWqlUr49mTJk2yyZMnW9OmTSnuzuR3NwkOp512mktBGN10000W3g4Jf7HGjRsbwsRlihwQnghSBCP9vPnmmyOx+f+EuSIkEYAwPfHEE91+pAzZhks98cQTVrduXQsPv7Zr187iWfOuv/5623fffQ3mrE0WHvIdOnSoqx9mNWvWtPfff989JhEvEvGNO+yww4z33qxZM3vkkUeceGzfvr3je84557g6w21G2PIusTjuvffezr+NuhREQAREQAREoKIIJFWYjRkzxs4880xjQ3CroB7dd999du211xrWGITKueeeax999JEhQhAsWFYIYSHgm4ofGgIG6xIWqVtvvdWwLM2ZM8fw9/rggw8Mywr1IBgGDhzoi7ozw388G4HSvHlzJwTxjSNx6tSpbsjxkksuMZ5PO4MgsOOOO86w8GHtat26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9T1Ev4F05uCEGQJIQQREQAREQAREQAREoGIJSJhVLH89XQQKJKBEERABERCB7CIgYZZd71u9FQEREAEREAERSGECSRFmOBuyHdMdd9xhffv2tX/+858JuqxoERABERABERABERCBRASSIsymTp1qzzzzjP2///f/rEmTJtanTx+bNWtWomcqXgREQAREQATKhoBqFYE0J5AUYTZ58mTr0KGDdezY0c4880xr06aNvfPOO2mORs0XAREQAREQAREQgfIlkBRh9t///tcqV66c2/LNmzfbV199lXuvCxEQgRITUEEREAEREIEsIpAUYda2bVv7+9//btOnTzeGNSdNmmQ//fRTFmFUV0VABERABERABESg9ASSIsyOP/5451t2++2326BBg+zYY4+1hg0bxm+dYkVABERABERABERABOISSIowW7VqlXXv3t1Zy8aMGWM1a9a0evXqxX2gIkVABERABESgLAmobhFIZwJJEWbvvfee9erVy3GPICylAAAPW0lEQVRYtGiRMZR5zDHHuHsdREAEREAEREAEREAEikYgKcLs1FNPdU/r2LGjXXnllda5c2c3tOkidRABESglARUXAREQARHIFgJJEWZ16tSxp59+2p566ilj6YwuXbpkCz/1UwREQAREQAREQASSRiApwsy3platWlapUiV/m/CsBBEQAREQAREQAREQgfwEkirM8levGBEQAREQAREodwJ6oAikLQEJs7R9dWq4CIiACIiACIhAphGQMMu0N6r+ZCYB9UoEREAERCArCORs2rTJ1q1bl5KBtm3cuNEUNtqGDRvEIfItiMNG9x2IgziE/13U96DvQd9D9BvIBA45OOtXQHCTBIry3KyQx4V0cuvWrRYEQSG5Mj9ZHKLvWBzEIUogetT3IA5RAtGjvof05+CGMnfZZRdLxQDeqlWrWraHatWqZT0DvgFxiP5dEAdx4O+DD/oeEn0P0XjPKVvO+h6i7z2dOThhhgBSEAEREAEREAEREAERqFgCEmYVy19PF4EiE1BGERABERCBzCcgYZb571g9FAEREAEREAERSBMCpRZmY8aMsTfeeCNPd7/55hsbMmSI9ezZ01555RXbvHlznvTojY4iIAIiIAIiIAIiIAJhAiUWZosXL7bRo0fbwIEDbeXKlbl1MlX1pptusq+++spOPvlkt3cmIi03gy5EQAREQAREoDwI6BkikIYESizM5s+fb0uWLLEaNWrk6fb06dPd/aOPPmrHHXecdevWzV577TVjTTKXoIMIiIAIiIAIiIAIiEBcAiUWZp06dbI+ffpY8+bN81S8atUqa9asWW5c7dq13fXatWvdWQcREIESE1BBERABERCBDCdQYmGWiAvCjPVDfHrNmjXd5S+//OLOOoiACIiACIiACIiACMQnkHRhxmr+P/74Y+7Tfv31V3ddq1Ytd85z0I0IiIAIiIAIiIAIiEAugaQLsz333NO+/fbb3AdgQcMPrUqVKrlxuhABERABERCB8iCgZ4hAuhFIujBr2bKlMWNz1qxZtmbNGhsxYoQddthh6cZF7RUBERABERABERCBcieQdGHWqFEj6969u/Xo0cPOOuss+/777+36668v947pgSKQmQTUKxEQAREQgUwmUGphxsxMhFgYUufOne2tt96yF1980Z5//nmrXr266T8REAEREAEREAEREIGCCZRamCWqftddd7U6deokSs6N14UIiIAIiIAIiIAIiECUQJkJs2j1OoqACIiACIhAhRLQw0UgrQhImKXV61JjRUAEREAEREAEMpmAhFkmv131LTMJqFciIAIiIAIZSyCHPSzXrVtnqRho28aNG01ho23YsEEcIt+COGx034E4iEP430V9D/oe9D1Ev4FM4JDDSv0VHKyg52esJC5Gx7Zu3WpBEBSjRGZmFYfoexUHcYgSiB71PYhDlED0qO8h/Tm4ocxddtnFUjGAt2rVqpbtgb1Hs50B/ReH6N8FcRAH/j74oO+hKN9DNI9nlslnfQ/Rd53OHJwwQwApiIAIiIAIiIAIiIAIVCwBCbOK5a+ni0CJCKiQCIiACIhAZhKQMMvM96peiYAIiIAIiIAIpCGBUguzH3/80W699VZjBmW4/3PnzrUBAwaEowq4VpIIiIAIiIAIiIAIiECJhRlCbPLkyXbffffZjBkzbPPmzY7mmjVrbNy4cda/f3+bP3++i9NBBERABERABCqUgB4uAmlCoMTC7KeffrJp06bl6+Y333xj8+bNs8qVK+dLU4QIiIAIiIAIiIAIiEBiAiUWZjVr1rQ+ffrYtddem6f2ww47zMV36NAhT7xuREAEkkpAlYmACIiACGQggRILswxkoS6JgAiIgAiIgAiIQIUSSB1hVqEY9HAREAEREAEREAERqHgCEmYV/w7UAhEQAREQgXIgoEeIQDoQkDBLh7ekNoqACIiACIiACGQFgVILsyCIv7l2EASWk1Pq6k3/iYAIJCKgeBEQAREQgUwjUGrl1KBBA/vggw9s1113zcOGWZlPP/10njjdiIAIiIAIiIAIiIAIJCZQamGWuOrip6iECIiACIiACIiACGQzAQmzbH776rsIiIAIZBcB9VYEUp6AhFnKvyI1UAREQAREQAREIFsISJhly5tWPzOTgHolAiIgAiKQUQRyNm3aZOvWrUvJQNs2btxoChttw4YN4hD5FsRho/sOxEEcwv8u6nvQ96DvIfoNZAKHnEqVKlkKhXxtySgZXMLObN261YIg/rIkJawyLYuJQ/S1iYM4RAlEj/oexCFKIHrU95D+HNxQ5i677GKpGMBbtWpVy/ZQrVq1rGfANyAO0b8L4iAO/H3wQd9Dcb+HaH7PL9PO+h6i7zedOThhhgBSEAEREAEREAEREAERqFgCEmYVy19PF4FSE1AFIiACIiACmUNAwixz3qV6IgIiIAIiIAIikOYESi3MxowZY2+88UYeDIsXL7b+/fvbzTffbOPHj7f169fnSS/4RqkiIAIiIAIiIAIikJ0ESizMEF+jR4+2gQMH2sqVK3PprV271i6//HI3pf/UU0+16dOn26233pqbrgsREAEREAERqFACergIpDCBEguz+fPn25IlS6xGjRp5urdgwQKrXbu23X///damTRvr3r27LVq0yL799ts8+XQjAiIgAiIgAiIgAiKQl0CJhVmnTp2sT58+1rx58zw1NmnSxPr165cbhyhjKY699torN04XIiACSSWgykRABERABDKEQImFWaL+16xZ0xo0aGBbtmyxsWPHOl+zyy67zP7whz8kKqJ4ERABERABERABERCBCIGkC7NInc6/7LrrrrORI0fagw8+aOeccw7RRQ/KKQIiIAIiIAIiIAJZSCDpwuznn3+2Hj16GJazF154wVq2bJmFWNVlERABERCBVCagtolAqhJIujBjFuY333xjF110kTFDk2vC77//nqoM1C4REAEREAEREAERSAkCSRdmCxcutP/+97+GXxnizAfEWUr0WI0QgYwkoE6JgAiIgAhkAoFSCzNmZrIkhodxww032AcffJAvNGrUyGfRWQREQAREQAREQAREIA6BUguzOHUmJUqViIAIiIAIiIAIiEC2EZAwy7Y3rv6KgAiIgAhAQEEEUpKAhFlKvhY1SgREQAREQAREIBsJSJhl41tXnzOTgHolAiIgAiKQ9gRyNm3aZOvWrUvJQNs2btzoFqzN9vOGDRvEIfItiEP074M4iEP430R9D/oe9D1Ev4FM4JBTqVIlS9Hg2pX20jcJHdi6dasFQZCEmtK7CnGIvj9xEIcogehR34M4RAlEj/oe0p+DG8rcZZddLBUDeKtWrWrZHqpVq5b1DPgGxCH6d0EcxIG/Dz7oeyjN9xAt61lmwlnfQ/SdpjMHJ8wQQAoiIAIiIAIiIAIiIAIVS0DCrGL56+kikFQCqkwEREAERCC9CUiYpff7U+tFQAREQAREQAQyiECphdmYMWPsjTfeyINk1qxZdu+991qvXr1s4sSJ9vPPP+dJL/qNcoqACIiACIiACIhA9hAosTBbvHixjR492gYOHGgrV67MJbZkyRLr0aOHVa9e3Y4//nh75ZVX7NVXX81N14UIiIAIiIAIpAwBNUQEUoxAiYXZ/PnzDRFWo0aNPF2aO3euHX300Xb99ddbmzZt7KSTTrKpU6fmyaMbERABERABERABERCB/ARKLMw6depkffr0sebNm+ep9eyzz7a+ffu6BWsZ0sRa1qpVqzx5dCMCIlBmBFSxCIiACIhAGhMosTBL1OecnBwjfPTRR25I88cff7T69esnyq54ERABERABERABERCBbQSSLsy21WtnnHGGTZ482bp06eIsa2yv5NOKdVZmERABERABERABEcgSAkkXZoMHD7aXX37Z4WOrp7Zt27rr9evXu7MOIiACIiACIpBKBNQWEUglAkkXZvvtt5+NGzfOFixY4JbJmDBhgjVt2tRq1aqVSv1WW0RABERABERABEQg5QgkXZi1bNnS2KPqz3/+s51yyin2r3/9y6688sqU67gaJAKZS0A9EwEREAERSFcCpRZmzMzs3r17bv/ZBPbJJ59065eNHTvWhgwZYoccckhuui5EQAREQAREQAREQATiEyi1MItXLbMyGbqsWbNmvORix6mACIiACIiACIiACGQDgTIRZtkATn0UAREQARHIGALqiAikDAEJs5R5FWqICIiACIiACIhAthOQMMv2L0D9z0wC6pUIiIAIiEBaEshh4dd169a5LZRS7UzbNm7caAobbcOGDeIQ+RbEYaP7DsRBHML/Lup70Peg7yH6DWQCh5xKlSpZKodtcjerT1u3brUgCLKaAZ0XByiYiYM4RAlEj/oexCFKIHrU95D+HNxQ5i677GKpGMDL8hvZHlgXLtsZ0H9xqGriEGUgDuLANxAOpf/3YTvTcL3pdi0O0feYzhycMEMAKYiACIiACIiACIiACFQsAQmziuWvp4tAmRFQxSIgAiIgAulHQMIs/d6ZWiwCIiACIiACIpChBEotzMaMGWNvvPFGXDzffPONsWcmM4biZihWpDKLgAiIgAiIgAiIQGYTKLEwW7x4sY0ePdoGDhxoK1euzEfp999/t3vuuccWLFhg//vf//KlK0IEREAEREAEUoqAGiMCKUCgxMJs/vz5tmTJEqtRo0bcbgwfPtz22WefuGmKFAEREAEREAEREAERyE+gxMKsU6dO1qdPH2vevHm+WufOnWvvvfeeXXnllfnSFCECIlBuBPQgERABERCBNCNQYmGWqJ+sutu7d2/r2bOnWxstUT7Fi4AIiIAIiIAIiIAI5CWQdGH25JNPWt26dW3z5s322WefuadxXr9+vbsu1UGFRUAEREAEREAERCCDCSRdmG3ZssXt5ffYY4/Z008/7dAh1r766it3rYMIiIAIiIAIpCoBtUsEKppA0oXZbbfdZqNGjXLhiSeecP0bOnSoHXbYYe5aBxEQAREQAREQAREQgfgEki7M4j9GsSIgAhVDQE8VAREQARFIJwKlFmbMzOzevXvcPrOJ6AcffGC777573HRFioAIiIAIiIAIiIAIbCdQamG2varyudJTREAEREAEREAERCBTCUiYZeqbVb9EQAREQARKQkBlRKBCCUiYVSh+PVwEREAEREAEREAEthOQMNvOQlcikJkE1CsREAEREIG0IZCzadMmW7duXUoG2sZOAgobbcOGDW59uGxnIQ4b3XcgDuIQ/rdA34O+B30P0W8gEzj8fwAAAP//AW2S/wAAAAZJREFUAwALrrQ9akS7qAAAAABJRU5ErkJggg==)

Listing InfoProperty DetailsMediaAddress - LocationContact InfoMeta - Source Info

Each tab includes a category of property data (e.g., Listing Info, Contact Info) along with the **legal access requirements** for automated capture. Let me know if you’d like this converted into a live Google Sheet or embedded into a project management tool.

## Prompt:
is there an instagram marketplace with rental properties listed

## Response:
No, **Instagram does not have an official "Marketplace" feature for rental properties** like Facebook Marketplace. However, there is an **emerging informal ecosystem** of property listings on Instagram, particularly for rentals, driven by:

* * *

🧩 What Exists Today
--------------------

### 1\. **Informal Property Listings via Instagram Posts & Stories**

Many realtors, property managers, and landlords use Instagram accounts to post rental properties. These typically include:

*   Photos or video walkthroughs
*   Description (price, location, bedrooms, etc.)
*   Contact info or "DM for details"
*   Story Highlights (categorized by neighborhoods, types, or availability)
*   Geotags and hashtags (e.g., `#NYCRentals`, `#LAapartment`)

> ⚠️ These listings are not structured data — scraping or indexing them requires parsing images, captions, and comments.

* * *

### 2\. **Instagram Shop/Catalog Workarounds**

While Instagram offers product catalogs via **Instagram Shopping**, it's not natively designed for rentals. However, some agencies use:

*   **“Shoppable posts”** to link to properties (via third-party platforms or their websites)
*   **Catalog integrations via Meta Commerce Manager** — limited, and mostly for sales, not rentals

* * *

### 3\. **Realtor & Agency Pages with Rental Highlights**

Common examples:

*   Real estate influencers or agencies curating:
    *   “Now Renting” story highlights
    *   IGTV apartment tours
    *   Reels showcasing walkthroughs

Examples of tags and search terms:

*   `#apartmentforrent`, `#furnishedrental`, `#brooklynrentals`, `#shorttermrental`

* * *

### 4\. **Third-Party Aggregators Using Instagram Feeds**

Some startups and real estate sites:

*   Use Instagram posts from agents as lead generation tools
*   Build listings that include embedded or linked Instagram posts
*   Have Chrome extensions or tools to auto-tag & repost listings from agents

* * *

✅ Summary
---------

| Feature | Exists on Instagram? | Notes |
| --- | --- | --- |
| Official Marketplace | ❌ No | Use Facebook Marketplace instead |
| Structured Listings | ❌ No | Posts are unstructured |
| Listings by Agents | ✅ Yes | Widespread in stories/posts |
| Catalog Integration | ⚠️ Yes (limited) | Possible via Meta Commerce, not ideal |
| Hashtag Ecosystem | ✅ Yes | Used for discovery by renters |
| API Access to Listings | ❌ No | Private data, scraping needed for automation |

* * *

📌 Best Ways to Find Rentals on Instagram
-----------------------------------------

*   Search by hashtags: `#rentalsinla`, `#furnishedapartment`, `#roomforrent`
*   Use location tags (e.g., “Downtown Miami”)
*   Follow local agents or city-specific rental pages
*   Monitor story highlights from verified or active agents

* * *

If you're looking to **build an automated scraper or discovery tool** for Instagram rentals, I can help blueprint it based on hashtag/location monitoring + contact extraction + NLP enrichment.

Would you like a list of active accounts that post rentals in your target city or a system plan to capture this data?



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)