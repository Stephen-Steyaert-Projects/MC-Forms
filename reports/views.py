from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from config.auth import basic_auth_required
from .forms import IssueReportForm
from .models import IssueReport


def reports_form(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST)
        if form.is_valid():
            IssueReport.objects.create(
                mc_username=form.cleaned_data['mc_username'],
                mc_uuid=form.get_uuid(),
                short_description=form.cleaned_data['short_description'],
                long_description=form.cleaned_data['long_description'],
            )
            return redirect('reports:success')
    else:
        form = IssueReportForm()
    return render(request, 'reports/form.html', {'form': form})


def success(request):
    return render(request, 'reports/success.html')


@basic_auth_required
def submissions(request):
    cutoff = timezone.now() - timedelta(days=settings.SUBMISSION_DONE_DELETE_DAYS)
    IssueReport.objects.filter(is_done=True, done_at__lt=cutoff).delete()

    active = IssueReport.objects.filter(is_done=False).order_by('-submitted_at')
    done = IssueReport.objects.filter(is_done=True).order_by('-done_at')
    return render(request, 'reports/submissions.html', {'active': active, 'done': done})


@basic_auth_required
def mark_done(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(IssueReport, pk=pk)
        entry.is_done = True
        entry.done_at = timezone.now()
        entry.save()
    return redirect('reports:submissions')
