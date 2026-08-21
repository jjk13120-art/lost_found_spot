from django.http import JsonResponse
from reports.models import Report
from django.contrib.auth.models import User
from django.db.models import Count
from scraping.utils import scrape_lost_items
from collections import Counter
import re

# Simple list of common place keywords (extend as needed)
COMMON_LOCATIONS = [
    "New York", "London", "Delhi", "Paris", "Berlin", "Tokyo", "Mumbai", "Los Angeles",
    "Chicago", "Toronto", "Munich", "Sydney", "Pune", "Bangalore"
]

def extract_location_from_title(title: str) -> str:
    """Return a guessed location from title or 'Reddit' if not found."""
    for loc in COMMON_LOCATIONS:
        if re.search(rf"\b{re.escape(loc)}\b", title, re.IGNORECASE):
            return loc
    return "Reddit"

def report_data_api(request):
    # Database counts
    status_data = Report.objects.values('status').annotate(count=Count('status'))
    location_data = Report.objects.values('location').annotate(count=Count('location'))
    total_reports = Report.objects.count()

    # Scraped Reddit posts
    scraped_items = scrape_lost_items()

    # Status counts from scraped items
    scraped_status_counts = Counter(
        item.get('status', '') for item in scraped_items if item.get('status')
    )

    # Location counts from scraped items (try to guess from title)
    guessed_locations = [
        extract_location_from_title(item.get('title', '')) for item in scraped_items
    ]
    scraped_location_counts = Counter(guessed_locations)

    # Merge status
    combined_status = Counter({row['status']: row['count'] for row in status_data})
    combined_status.update(scraped_status_counts)

    # Merge locations
    combined_locations = Counter({row['location']: row['count'] for row in location_data})
    combined_locations.update(scraped_location_counts)

    # Convert to list
    combined_status_data = [{"status": s, "count": c} for s, c in combined_status.items()]
    combined_location_data = [{"location": loc, "count": c} for loc, c in combined_locations.items()]

    combined_total = total_reports + len(scraped_items)

    return JsonResponse({
        "status_data": combined_status_data,
        "location_data": combined_location_data,
        "report_count": combined_total,
        "scraped_count": len(scraped_items)
    })


def user_count_api(request):
    user_count = User.objects.count()
    return JsonResponse({"user_count": user_count})
