# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.models import SpeakerProfile

@login_required
def speaker_follow(request, username):
    speaker = get_object_or_404(SpeakerProfile, user__username=username)
    user_profile = request.user.get_profile()

    speaker.followers.add(user_profile)
    speaker.save()

    user_profile.following.add(speaker)
    user_profile.save()

    if request.GET['last']:
        return redirect(request.GET['last'])
    else:
        return redirect('/')