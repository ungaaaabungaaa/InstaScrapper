import instaloader
import os
import time
import random
import re
import requests

# To avoid blocks, we use:
# 1. Random delays between posts and accounts.
# 2. Batching (10 accounts per batch).
# 3. Proxy rotation (if proxies.txt is provided).

def clean_username(raw_name):
    """Removes @ and any leading/trailing whitespace or special characters."""
    # Remove any non-standard invisible characters first
    name = raw_name.strip()
    
    # Remove @ wherever it is (usually start)
    name = name.replace("@", "")
    
    # Remove any non-alphanumeric characters except dots and underscores
    name = re.sub(r'[^a-zA-Z0-9._]', '', name)
    return name

def get_usernames_from_file(file_path):
    """Reads usernames from a file, one per line."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found in {os.getcwd()}")
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print(f"Read {len(lines)} lines from {file_path}")
    
    usernames = []
    for line in lines:
        cleaned = clean_username(line)
        if cleaned:
            usernames.append(cleaned)
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(usernames))

def load_proxies(file_path="proxies.txt"):
    """Loads proxies from a file. Format: ip:port or user:pass@ip:port"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scrape_instagram_photos(usernames, batch_size=10, delay_between_batches=3600, use_proxies=False):
    """
    Scrapes photos in batches with delays and optional proxy rotation.
    """
    L = instaloader.Instaloader(
        download_videos=False, 
        download_video_thumbnails=False,
        download_geotags=False, 
        download_comments=False, 
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern=None, # Disable .txt caption files
        quiet=False
    )

    proxies = load_proxies() if use_proxies else []
    proxy_index = 0

    total_users = len(usernames)
    print(f"Total unique users found: {total_users}")

    for i in range(0, total_users, batch_size):
        batch = usernames[i:i + batch_size]
        print(f"\n--- Starting Batch {i//batch_size + 1} (Processing {len(batch)} users) ---")
        
        for username in batch:
            # IP Rotation logic
            if proxies:
                current_proxy = proxies[proxy_index % len(proxies)]
                os.environ['HTTP_PROXY'] = f"http://{current_proxy}"
                os.environ['HTTPS_PROXY'] = f"http://{current_proxy}"
                print(f"Using proxy: {current_proxy}")
                proxy_index += 1

            print(f"Scraping: {username}")
            target_folder = username
            
            try:
                profile = instaloader.Profile.from_username(L.context, username)
                
                count = 0
                max_photos = 100 # Limit to 100 photos per profile
                
                for post in profile.get_posts():
                    if count >= max_photos:
                        print(f"Reached limit of {max_photos} photos for {username}")
                        break
                        
                    if not post.is_video:
                        L.download_post(post, target=target_folder)
                        count += 1
                        # Human-like delay between post downloads
                        time.sleep(random.uniform(3, 7))
                
                print(f"Finished {username}: {count} photos.")
                
                # Delay between different accounts
                account_delay = random.uniform(45, 120)
                print(f"Waiting {account_delay:.2f}s before next account...")
                time.sleep(account_delay)

            except instaloader.exceptions.ProfileNotExistsException:
                print(f"Error: Profile {username} does not exist.")
            except instaloader.exceptions.QueryReturnedBadRequestException:
                print(f"Error: Rate limited or bad request. Waiting 10 minutes...")
                time.sleep(600)
            except Exception as e:
                print(f"An error occurred while scraping {username}: {e}")
                time.sleep(60)

        # Batch delay
        if i + batch_size < total_users:
            # If you want to spread 5 batches over 24 hours, delay should be ~4.8 hours
            # But here we use the user's suggestion or a reasonable default.
            wait_min = delay_between_batches / 60
            print(f"\nBatch complete. Next batch in {wait_min:.1f} minutes...")
            time.sleep(delay_between_batches)

if __name__ == "__main__":
    list_file = "list.txt"
    all_users = get_usernames_from_file(list_file)
    
    if all_users:
        # To run just the FIRST 10 accounts once and exit, uncomment the line below:
        all_users = all_users[:10]
        
        # Configuration:
        # Batch size: 10
        # Delay between batches: 3600s (1 hour)
        # Set use_proxies=True if you create a proxies.txt file
        scrape_instagram_photos(all_users, batch_size=10, delay_between_batches=3600, use_proxies=False)
    else:
        print("No users found in list.txt")
