from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk, TalkSlideDeck
from talks.forms import TalkSlideDeckForm
from talks.models.choices import *

@login_required
def talk_slides_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkSlideDeckForm(request.POST)

        if form.is_valid():
            deck = TalkSlideDeck()
            deck.talk = talk

            embed = form.cleaned_data['embed']
            embed = embed.split(' ')
            embed = [x.split('=') for x in embed]
            embed = [x for x in embed if len(x) == 2]
            embed = {x[0]: x[1].strip(""" "'""") for x in embed}

            deck.source = form.cleaned_data['source']

            if deck.source == SLIDESHARE:
                deck.data = embed['src']
                w = embed['width']
                h = embed['height']
                deck.aspect = int(w) / float(h) if float(h) != 0 else 0
            elif deck.source == SPEAKERDECK:
                deck.data = embed['data-id']
                deck.aspect = float(embed['data-ratio'])
            else:
                return HttpResponseNotFound()

            deck.save()

            return redirect(talk)

    return HttpResponseNotFound()
