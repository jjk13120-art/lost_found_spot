# reports/views.py

from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from scraping.utils import scrape_lost_items

@login_required
def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('reports:my_reports')
    else:
        form = ReportForm()
    return render(request, 'reports/submit_report.html', {'form': form})

@login_required
def my_reports(request):
    # Local DB reports
    reports = Report.objects.all()

    # Get filters
    query = request.GET.get('q')
    status = request.GET.get('status')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    sort = request.GET.get('sort')

    # Scrape Reddit posts
    scraped_items = scrape_lost_items()

    # Apply filters to local reports
    if query:
        reports = reports.filter(
            Q(category__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if status:
        reports = reports.filter(status=status)

    if from_date:
        reports = reports.filter(date_reported__gte=from_date)

    if to_date:
        reports = reports.filter(date_reported__lte=to_date)

    if sort == 'oldest':
        reports = reports.order_by('date_reported')
    else:
        reports = reports.order_by('-date_reported')  # Default to latest

    # --- Filter scraped_items as well ---
    if isinstance(scraped_items, list):
        # Filter by query
        if query:
            scraped_items = [
                i for i in scraped_items
                if query.lower() in i.get("title", "").lower()
            ]
        # Filter by status
        if status:
            scraped_items = [
                i for i in scraped_items
                if i.get("status", "").lower() == status.lower()
            ]
        # Sort scraped posts by date (if available)
        if sort == "oldest":
            scraped_items.sort(key=lambda x: x.get("date", ""))
        else:
            scraped_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    return render(request, 'reports/my_reports.html', {
        'reports': reports,
        'scraped_items': scraped_items
    })


@login_required
def user_reports(request):
    query = request.GET.get('q')
    if query:
        reports = Report.objects.filter(
            Q(category__icontains=query) | Q(description__icontains=query),
            user=request.user
        )
    else:
        reports = Report.objects.all()
    return render(request, 'reports/my_reports.html', {'reports': reports})

