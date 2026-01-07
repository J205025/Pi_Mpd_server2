import feedparser
from typing import List, Dict

def parse_rss_feed(feed_url: str) -> Dict:
    """
    Fetches and parses an RSS feed from the given URL.

    Args:
        feed_url: The URL of the RSS feed.

    Returns:
        A dictionary containing feed information and a list of episodes.
    """
    feed = feedparser.parse(feed_url)

    # Extract feed-level information
    feed_info = {
        "title": feed.feed.get("title"),
        "link": feed.feed.get("link"),
        "description": feed.feed.get("description"),
        "image": feed.feed.get("image", {}).get("href")
        or feed.feed.get("itunes_image")
        or (feed.feed.get("image") and feed.feed.image.get("href")),
    }

    episodes = []
    for entry in feed.entries:
        episode = {
            "id": entry.get("id") or entry.get("guid"),
            "title": entry.get("title"),
            "published": entry.get("published"),
            "link": entry.get("link"),
            "description": entry.get("description"),
            "summary": entry.get("summary") or entry.get("itunes_summary"),
            "image": entry.get("image", {}).get("href")
            or entry.get("itunes_image")
            or (entry.get("image") and entry.image.get("href")),
            "audio_url": None,
            "audio_length": None,
            "audio_type": None,
            "duration": entry.get("itunes_duration"),
        }

        if "enclosures" in entry and len(entry.enclosures) > 0:
            enclosure = entry.enclosures[0]
            episode["audio_url"] = enclosure.get("href")
            episode["audio_length"] = enclosure.get("length")
            episode["audio_type"] = enclosure.get("type")

        episodes.append(episode)

    return {"feed_info": feed_info, "episodes": episodes}

