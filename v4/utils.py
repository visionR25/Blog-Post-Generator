# This script provides utility functions for saving, loading, listing, and deleting blog posts.
import os
import logging
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

# Get absolute path to current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saved_blogs")
os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure folder exists

def _make_filename(topic):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_").lower()
    return f"{safe_topic}_{timestamp}.json"

def save_blog(topic, blog_text, metadata):
    logging.debug(f"Saving blog for topic: {topic}, metadata: {metadata}")
    filename = _make_filename(topic)
    full_data = {
        "topic": topic,
        "content": blog_text,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat()
    }
    full_path = os.path.join(SAVE_DIR, filename)  # Ensure it saves to the saved_blogs folder
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    return filename

def list_saved_blogs():
    files = sorted(os.listdir(SAVE_DIR), reverse=True)
    return [f for f in files if f.endswith(".json")]

def load_blog(filename):
    full_path = os.path.join(SAVE_DIR, filename)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_blog(filename):
    full_path = os.path.join(SAVE_DIR, filename)
    if os.path.exists(full_path):
        os.remove(full_path)

def export_to_pdf(topic, content):
    filename = f"{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("saved_blogs", filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    lines = content.split("\n")
    y = height - 50

    for line in lines:
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(50, y, line[:110])  # limit line length for page width
        y -= 15

    c.save()
    return filepath

def export_to_markdown(topic, content):
    filename = f"{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join("saved_blogs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath
