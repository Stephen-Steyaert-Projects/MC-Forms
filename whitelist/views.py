from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from config.auth import basic_auth_required
from .forms import WhitelistForm
from .models import WhitelistRequest


def whitelist_form(request):
    if request.method == 'POST':
        form = WhitelistForm(request.POST)
        if form.is_valid():
            WhitelistRequest.objects.create(
                mc_username=form.cleaned_data['mc_username'],
                mc_uuid=form.get_uuid(),
                discord_handle=form.cleaned_data['discord_handle'],
                reason=form.cleaned_data.get('reason', ''),
            )
            return redirect('whitelist:success')
    else:
        form = WhitelistForm()
    return render(request, 'whitelist/form.html', {'form': form})


def success(request):
    return render(request, 'whitelist/success.html')


@basic_auth_required
def submissions(request):
    cutoff = timezone.now() - timedelta(days=settings.SUBMISSION_DONE_DELETE_DAYS)
    WhitelistRequest.objects.filter(is_done=True, done_at__lt=cutoff).delete()

    active = WhitelistRequest.objects.filter(is_done=False).order_by('-submitted_at')
    done = WhitelistRequest.objects.filter(is_done=True).order_by('-done_at')
    return render(request, 'whitelist/submissions.html', {'active': active, 'done': done})


@basic_auth_required
def mark_done(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(WhitelistRequest, pk=pk)
        entry.is_done = True
        entry.done_at = timezone.now()
        entry.save()
    return redirect('whitelist:submissions')
