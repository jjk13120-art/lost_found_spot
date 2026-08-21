import os
from bs4 import BeautifulSoup

def scrape_lost_items():
    """
    Parse the saved Reddit HTML and extract:
    - title
    - link
    - image (main or thumbnail)
    - date
    - status (Lost / Found)
    """
    html_path = os.path.join(os.path.dirname(__file__), "lostandfound_full.html")

    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        base_url = "https://www.reddit.com"
        items = []

        # Modern Reddit posts (preferred)
        posts = soup.select("div[data-testid='post-container']")
        if not posts:
            # Fallback for old static dump
            posts = soup.select("shreddit-post")

        for post in posts:
            # Title
            title_tag = post.select_one("faceplate-screen-reader-content")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            # Link
            link_tag = post.select_one("a.absolute")
            link = base_url + link_tag.get("href", "") if link_tag else "#"

            # Status from flair
            flair_tag = post.select_one("div.flair-content")
            status = flair_tag.get_text(strip=True) if flair_tag else "Unspecified"

            # Main image (if available)
            img_tag = post.select_one("img#post-image")

            # Thumbnail fallback
            if not img_tag:
                img_tag = post.select_one("div[slot='thumbnail'] img")

            image = img_tag.get("src", "") if img_tag else ""

            # Date/time
            time_tag = post.select_one("time")
            date = time_tag.get("datetime", "") if time_tag else ""

            # Avoid duplicates (unique link)
            if any(i["link"] == link for i in items):
                continue

            items.append({
                "title": title,
                "link": link,
                "status": status,
                "image": image,
                "date": date
            })

        return items

    except Exception as e:
        return [{"error": f"Failed to read saved HTML: {e}"}]
