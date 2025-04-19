# This script is the main logic for fetching trending keywords using SerpAPI.
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()  # For API key in .env file

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def get_serpapi_trends(topic, region="uk"):
    try:
        search = GoogleSearch({
            "q": topic,
            "location": "United Kingdom",
            "hl": "en",
            "gl": region,
            "api_key": SERPAPI_KEY
        })
        result = search.get_dict()
        
        if "related_questions" in result:
            return [q["question"] for q in result["related_questions"][:5]]
        
        if "related_searches" in result:
            return [s["query"] for s in result["related_searches"][:5]]

    except Exception as e:
        print(f"SerpAPI error: {e}")
        return _fallback_keywords(topic)

    return _fallback_keywords(topic)

def _fallback_keywords(topic):
    return [
        f"{topic} trends",
        f"{topic} 2025",
        f"future of {topic}",
        f"{topic} use cases",
        f"{topic} examples"
    ]
