from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Story, Feedback
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def submit_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    stories = Story.objects.all().order_by('-submitted_at')


    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user

            # If name is empty, use user's username
            if not feedback.name:
                feedback.name = request.user.username

            feedback.save()
            return redirect('feedback:feedback')  # FIXED: use namespace
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'feedbacks': feedbacks,
        'stories': stories,  # Pass stories to template
    }
    return render(request, 'feedback/submit_feedback.html', context)

@login_required
def share_story(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Story.objects.create(user=request.user, title=title, content=content)
            messages.success(request, "Your story has been shared successfully!")
        else:
            messages.error(request, "Please fill in all fields.")

    return redirect('feedback:feedback')  # FIXED: use namespace
