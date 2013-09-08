from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q, Count

from engagements.models import Engagement
from core.helpers import render_to

from core.models import SpkrbarUser
from events.models import Event
from talks.models import Talk

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    engagements = event.engagements.all()

    if request.user.is_anonymous():
        engagements = engagements.filter(talk__published=True)
    else:
        engagements = engagements.filter(
                Q(talk__published=True) | 
                Q(talk__speaker=request.user))

    yesterday = datetime.today() - timedelta(days=1)
    tomorrow = datetime.today() + timedelta(days=1)
    current = engagements.filter(date__gt=yesterday, date__lt=tomorrow).order_by('date')
    upcoming = engagements.filter(date__gt=tomorrow).order_by('date')
    past = engagements.filter(date__lt=yesterday).order_by('-date')

    speakers = SpkrbarUser.objects.filter(talk__in=[e.talk for e in engagements]).distinct()
    speakers = speakers.annotate(
            num_tags=Count('tags'),
            num_links=Count('links')).order_by(
                    '-photo', '-about_me', '-num_tags', '-num_links')[:20]

    if not request.user.is_anonymous():
        user_talks = Talk.objects.filter(speaker=request.user.get_profile())
    else:
        user_talks = None

    context = {
        'event': event,
        'user_talks': user_talks,
        'querystring': event.location.geocode_querystring(),
        'city_querystring': event.location.geocode_city_querystring(),
        'current': current,
        'upcoming': upcoming,
        'past': past,
        'speakers': speakers,
        'last': event.get_absolute_url()
        }

    return render_to(request, 'events/event_detail.haml', context=context)
