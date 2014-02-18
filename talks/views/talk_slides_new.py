from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk, TalkSlideDeck
from talks.forms import TalkSlideDeckForm
from talks.models.choices import *

@login_required
def talk_slides_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.user != talk.speaker:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkSlideDeckForm(request.POST)

        if form.is_valid():
            deck = TalkSlideDeck.from_embed(talk, form.cleaned_data['embed'], form.cleaned_data['source'])

            if deck:
                deck.save()
                return redirect(talk)
            else:
                return HttpResponseNotFound()


    return HttpResponseNotFound()
