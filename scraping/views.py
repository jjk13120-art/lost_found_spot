from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import scrape_lost_items

@login_required
def scraped_items(request):
    posts = scrape_lost_items()
    return render(request, "scraping/scraped_items.html", {"posts": posts})
