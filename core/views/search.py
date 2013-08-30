import random
from datetime import datetime
from django.db.models import Q
from django.shortcuts import redirect

from core.helpers import template

from talks.models import TalkTag
from talkevents.models import TalkEvent
from core.models import SpeakerProfile, AttendeeProfile, ProfileTag
from events.models import Event

@template('search.haml')
def search(request):
    if 'query' not in request.GET:
        return redirect('/')

    query = request.GET['query']

    if len(query) < 3:
        return redirect('/')

    talk_tags = TalkTag.objects.filter(name__icontains=query)

    talks = TalkEvent.objects.filter(
            Q(talk__published=True), 
            Q(date__gte=datetime.today()),
            Q(talk__name__icontains=query) | 
            Q(event__owner__name__icontains=query) | 
            Q(talk__tags__in=talk_tags))

    events = Event.objects.filter(
            Q(owner__name__icontains=query) |
            Q(name__icontains=query) |
            Q(location__name__icontains=query))

    profile_tags = ProfileTag.objects.filter(name__icontains=query)

    speakers = SpeakerProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(tags__in=profile_tags))

    attendees = AttendeeProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(tags__in=profile_tags))

    if talks.count() > 12:
        talks = random.sample(talks, 12)

    if events.count() > 12:
        events = random.sample(events, 12)

    if speakers.count() > 12:
        speakers = random.sample(speakers, 12)

    if attendees.count() > 12:
        attendees = random.sample(attendees, 12)

    return {'talks': talks,
            'events': events,
            'speakers': speakers,
            'attendees': attendees}
