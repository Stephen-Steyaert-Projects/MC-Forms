from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from config.auth import basic_auth_required
from .forms import RecommendationForm
from .models import Recommendation


def recs_form(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            Recommendation.objects.create(
                mc_username=form.cleaned_data['mc_username'],
                mc_uuid=form.get_uuid(),
                recommendation=form.cleaned_data['recommendation'],
            )
            return redirect('recs:success')
    else:
        form = RecommendationForm()
    return render(request, 'recs/form.html', {'form': form})


def success(request):
    return render(request, 'recs/success.html')


@basic_auth_required
def submissions(request):
    cutoff = timezone.now() - timedelta(days=settings.SUBMISSION_DONE_DELETE_DAYS)
    Recommendation.objects.filter(is_done=True, done_at__lt=cutoff).delete()

    active = Recommendation.objects.filter(is_done=False).order_by('-submitted_at')
    done = Recommendation.objects.filter(is_done=True).order_by('-done_at')
    return render(request, 'recs/submissions.html', {'active': active, 'done': done})


@basic_auth_required
def mark_done(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(Recommendation, pk=pk)
        entry.is_done = True
        entry.done_at = timezone.now()
        entry.save()
    return redirect('recs:submissions')
