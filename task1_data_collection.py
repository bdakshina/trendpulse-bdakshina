import requests
import json
import os
import time
import re
from datetime import datetime

HEADERS = {"User-Agent": "TrendPulse/1.0"}
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"

CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_trending_data():
    print("Fetching top 500 story IDs...")
    
    session = requests.Session()
    
    try:
        response = session.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        top_ids = response.json()[:500]
    except requests.RequestException as e:
        print(f"Failed to fetch top stories: {e}")
        return

    collected_stories = []
    fetched_items_cache = {}
    used_ids = set()
    
    for category, keywords in CATEGORIES.items():
        print(f"Scanning for category: {category}...")
        stories_found = 0
        
        for story_id in top_ids:
            if stories_found >= 25:
                break
            
            if story_id in used_ids:
                continue

            # Fetch the story details if we haven't already
            if story_id not in fetched_items_cache:
                try:
                    # Live progress indicator
                    print(f"  Fetching story details for ID {story_id}...", end="\r", flush=True)
                    
                    resp = session.get(ITEM_URL_TEMPLATE.format(story_id), headers=HEADERS)
                    resp.raise_for_status()
                    fetched_items_cache[story_id] = resp.json()
                except requests.RequestException as e:
                    # If request fails, print message and move on (Requirement 1)
                    print(f"\nFailed to fetch story {story_id}: {e}")
                    continue
            
            story = fetched_items_cache[story_id]
            
            # Skip invalid data
            if not story or 'title' not in story or story.get('type') != 'story':
                continue

            title = story['title']
            
            # Check for keywords using regex to match whole words (case-insensitive)
            matched = False
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', title, re.IGNORECASE):
                    matched = True
                    break
            
            if matched:
                # Extract the required fields (Requirement 2)
                collected_stories.append({
                    "post_id": story.get('id'),
                    "title": title,
                    "category": category,
                    "score": story.get('score', 0),
                    "num_comments": story.get('descendants', 0),
                    "author": story.get('by', 'Unknown'),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                used_ids.add(story_id)
                stories_found += 1
        
        # Clear the progress line and print the summary for the category
        print(" " * 50, end="\r") 
        print(f"Finished {category} (Found: {stories_found}). Waiting 2 seconds...\n")
        
        # Wait 2 seconds between each category loop (Requirement 1)
        time.sleep(2)

    os.makedirs("data", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)
        
    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    fetch_trending_data()