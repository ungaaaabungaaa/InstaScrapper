# Instagram Photo Scraper

A robust Python script to scrape public photos from a list of Instagram usernames. Built with `instaloader`, it includes anti-blocking features like batching, random delays, and optional proxy rotation.

## Features
- **Automated Batching**: Processes accounts in batches (default: 10) with long delays between batches.
- **Human-like Behavior**: Random delays between post downloads and account switches.
- **Username Cleaning**: Automatically handles `@` symbols and hidden characters in your input list.
- **Proxy Support**: Optional IP rotation using a `proxies.txt` file.
- **Folder Organization**: Downloads photos into folders named after each username.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd InstaScrape
```

### 2. Create and Activate Virtual Environment
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Use

### 1. Add Usernames
Open `list.txt` and add the Instagram usernames you want to scrape, one per line. You can include the `@` symbol or not; the script handles both.
Example:
```text
@nike
@adidas
zara
```

### 2. Configure the Script (Optional)
Open `scrape_insta.py` to adjust settings:
- **Test Mode**: Uncomment `all_users = all_users[:10]` at the bottom to only run the first 10 accounts.
- **Batch Size**: Change `batch_size=10` in the `scrape_instagram_photos` call.
- **Delay**: Change `delay_between_batches=3600` (default is 1 hour).

### 3. Run the Scraper
```bash
python scrape_insta.py
```

---

## Anti-Blocking Tips
- **Proxies**: If you have proxies, add them to `proxies.txt` (one per line, format `ip:port` or `user:pass@ip:port`) and set `use_proxies=True` in `scrape_insta.py`.
- **Timing**: The script is designed to run over a long period (e.g., 24 hours). Don't set the delays too low, or Instagram may temporarily block your IP.
- **Login**: This script works for public profiles without logging in. Scaping private profiles or very high volumes requires authentication, which is not enabled by default to protect your account from being flagged.

## Disclaimer
This tool is for educational purposes only. Please respect Instagram's Terms of Service and the privacy of users.

