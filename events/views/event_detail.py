from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q

from talkevents.models import TalkEvent
from core.helpers import render_to

from events.models import Event
from talks.models import Talk

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    talk_events = TalkEvent.objects.filter(event=event)

    if request.user.is_anonymous():
        talk_events = talk_events.filter(talk__published=True)
    else:
        talk_events = talk_events.filter(
                Q(talk__published=True) | 
                Q(talk__speaker=request.user))

    user_attending = False

    attendees = event.attendees.all()
    endorsements = event.endorsements.all()
    user_attending = (request.user in attendees)
    user_endorsed = (request.user in endorsements)

    will_have_links = not user_attending or not user_endorsed

    yesterday = datetime.today() - timedelta(days=1)
    tomorrow = datetime.today() + timedelta(days=1)
    current = talk_events.filter(date__gt=yesterday, date__lt=tomorrow).order_by('date')
    upcoming = talk_events.filter(date__gt=tomorrow).order_by('date')
    recent = talk_events.filter(
            date__gt=(yesterday - timedelta(days=14)), date__lt=yesterday
                ).order_by('-date')

    if not request.user.is_anonymous():
        user_talks = Talk.objects.filter(speaker=request.user.get_profile())
    else:
        user_talks = None

    context = {
        'event': event,
        'attendees': attendees,
        'endorsements': endorsements,
        'user_attending': user_attending,
        'user_endorsed': user_endorsed,
        'user_talks': user_talks,
        'will_have_links': will_have_links,
        'querystring': event.location.geocode_querystring(),
        'city_querystring': event.location.geocode_city_querystring(),
        'current': current,
        'upcoming': upcoming,
        'recent': recent,
        'last': event.get_absolute_url()
        }

    return render_to(request, 'events/event_detail.haml', context=context)
