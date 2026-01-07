import feedparser
import requests
import os
import re
from datetime import datetime, timedelta
import time
import ssl

# --- FIX 1: Bypass SSL certificate verification issues ---
# This prevents feedparser from failing on certain HTTPS setups
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Define the podcast RSS feeds
podcast_rss = {
   "BBC_GlobalNewsPodcast" : "https://podcasts.files.bbci.co.uk/p02nq0gn.rss",
   "NewYorkTimes_TheDaily" : "https://feeds.simplecast.com/54nAGcIl",
   "BBC_WorldBusinessReport" : "https://podcasts.files.bbci.co.uk/p02tb8vq.rss",
   "Economist_Economist" : "https://access.acast.com/rss/ec380acc-fe13-46a0-991f-a1e508d126f8"
}

# Define the base directory
base_dir = "/home/ubuntu/Music/播客/"
os.makedirs(base_dir, exist_ok=True)

# Define time thresholds
file_age_threshold = 30 
seven_days_ago = datetime.now() - timedelta(days=7)
thirty_days_ago = datetime.now() - timedelta(days=file_age_threshold)

# --- FIX 2: Added User-Agent header ---
# Servers often block scripts that don't identify as a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clean_old_files(directory, age_threshold):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < age_threshold:
                try:
                    os.remove(file_path)
                    print(f"🧹 Removed old file: '{filename}'")
                except OSError as e:
                    print(f"Error removing file {filename}: {e}")

print("Starting cleanup...")
for podcast_name in podcast_rss.keys():
    podcast_dir = os.path.join(base_dir, podcast_name)
    if os.path.exists(podcast_dir):
        clean_old_files(podcast_dir, thirty_days_ago)

for podcast_name, feed_url in podcast_rss.items():
    print(f"\n--- Processing: {podcast_name} ---")
    podcast_dir = os.path.join(base_dir, podcast_name)
    os.makedirs(podcast_dir, exist_ok=True)
    
    # --- FIX 3: Robust Parsing & Debugging ---
    feed = feedparser.parse(feed_url)
    
    # Check if feed failed to load
    if not feed.entries:
        print(f"⚠️ No entries found for {podcast_name}. Check if the URL is correct or if you are being blocked.")
        continue
    
    print(f"Found {len(feed.entries)} total episodes in feed.")

    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            
            # If you want to test the script, you could temporarily comment out these two lines
            if pub_date < seven_days_ago:
                continue

        audio_link = None
        if hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if enclosure.get('type') in ['audio/mpeg', 'audio/mp4', 'audio/x-m4a']:
                    audio_link = enclosure.get('href')
                    break
        
        if audio_link:
            title = entry.title
            pub_date_str = pub_date.strftime('%Y-%m-%d')
            sanitized_title = re.sub(r'[\\/:*?"<>|]', '', title)
            file_name = f"{pub_date_str} - {sanitized_title}.mp3"
            file_path = os.path.join(podcast_dir, file_name)
            
            if os.path.exists(file_path):
                print(f"⏩ Skipping: '{title}' (Already exists)")
                continue

            print(f"📥 Downloading: '{title}'...")
            try:
                # Apply the headers here
                with requests.get(audio_link, stream=True, headers=headers, timeout=30) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"✅ Success!")
            except Exception as e:
                print(f"❌ Failed: {e}")
        else:
            print(f"⚠️ No audio found for '{entry.title}'")