import feedparser
import requests
import os
import re
from datetime import datetime, timedelta
import time

# Define the podcast RSS feeds
podcast_rss = {
   "BBC_GlobalNewsPodcast" : "https://podcasts.files.bbci.co.uk/p02nq0gn.rss",
   "NewYorkTimes_TheDaily" : "https://feeds.simplecast.com/54nAGcIl"
   #"BBC_World_BusinessReport" : "https://podcasts.files.bbci.co.uk/p02tb8vq.rss"
   #"Economist_Economist" : "https://access.acast.com/rss/ec380acc-fe13-46a0-991f-a1e508d126f8"
      }

# Define the base directory for all podcasts
base_dir = "/home/ubuntu/Music/播客/"
os.makedirs(base_dir, exist_ok=True)

# Define the age threshold for keeping files
file_age_threshold = 30 # days
seven_days_ago = datetime.now() - timedelta(days=7)
thirty_days_ago = datetime.now() - timedelta(days=file_age_threshold)

def clean_old_files(directory, age_threshold):
    """
    Removes files from a directory that are older than the specified age threshold.
    """
    now = datetime.now()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < age_threshold:
                try:
                    os.remove(file_path)
                    print(f"🧹 Removed old file: '{filename}'")
                except OSError as e:
                    print(f"Error removing file {filename}: {e}")

# --- Main Script Logic ---

# First, run the cleanup for all existing podcast folders
print("Starting cleanup of old podcast files...")
for podcast_name in podcast_rss.keys():
    podcast_dir = os.path.join(base_dir, podcast_name)
    if os.path.exists(podcast_dir):
        clean_old_files(podcast_dir, thirty_days_ago)
print("Cleanup complete.")

# Now, proceed with downloading new episodes
for podcast_name, feed_url in podcast_rss.items():
    print(f"\n--- Processing: {podcast_name} ---")
    
    # Create a unique subdirectory for each podcast inside the base directory
    podcast_dir = os.path.join(base_dir, podcast_name)
    os.makedirs(podcast_dir, exist_ok=True)
    print(f"Podcast files will be saved in the '{podcast_dir}' directory.")
    
    # Parse the RSS feed
    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        print(f"Error parsing feed {podcast_name}: {e}")
        continue
    
    # Iterate through each episode in the feed
    for entry in feed.entries:
        # Check if the episode was published within the last 7 days
        if hasattr(entry, 'published_parsed'):
            pub_timestamp = time.mktime(entry.published_parsed)
            pub_date = datetime.fromtimestamp(pub_timestamp)
            
            if pub_date < seven_days_ago:
                print(f"Skipping '{entry.title}': Published on {pub_date.strftime('%Y-%m-%d')}, which is older than 7 days.")
                continue

        # Check for the audio enclosure
        audio_link = None
        if hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if enclosure.get('type') in ['audio/mpeg', 'audio/mp4']:
                    audio_link = enclosure.get('href')
                    break
        
        # If an audio link is found, download the file
        if audio_link:
            title = entry.title
            # Sanitize the title and prepend the publication date
            pub_date_str = pub_date.strftime('%Y-%m-%d')
            sanitized_title = re.sub(r'[\\/:*?"<>|]', '', title)
            file_name = f"{pub_date_str} - {sanitized_title}.mp3"
            file_path = os.path.join(podcast_dir, file_name)
            
            # Check if the file already exists to avoid re-downloading
            if os.path.exists(file_path):
                print(f"Skipping '{title}': File already exists.")
                continue

            print(f"Downloading '{title}'...")
            
            try:
                with requests.get(audio_link, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"✅ Successfully downloaded '{title}'")
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to download '{title}': {e}")
        else:
            print(f"⚠️ No audio link found for '{entry.title}'")