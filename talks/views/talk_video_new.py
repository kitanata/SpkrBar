from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk, TalkVideo
from talks.forms import TalkVideoForm
from talks.models.choices import *

@login_required
def talk_video_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.user != talk.speaker:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkVideoForm(request.POST)

        if form.is_valid():
            video = TalkVideo.from_embed(talk, form.cleaned_data['embed'])

            if video:
                video.save()
                return redirect(talks)
            else:
                return HttpResponseNotFound()

    return HttpResponseNotFound()
