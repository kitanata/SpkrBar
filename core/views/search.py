import random
import operator
from datetime import datetime
from django.db.models import Q
from django.shortcuts import redirect

from core.helpers import template, events_from_engagements

from talks.models import Talk, TalkTag
from engagements.models import Engagement
from core.models import SpkrbarUser, UserTag

@template('search.haml')
def search(request):
    if 'query' not in request.GET:
        return redirect('/')

    query = request.GET['query']

    query = query.split(' ')

    talk_tags = TalkTag.objects.filter(
        reduce(operator.and_, (Q(name__icontains=x) for x in query)))
    user_tags = UserTag.objects.filter(
        reduce(operator.and_, (Q(name__icontains=x) for x in query)))

    talks = Talk.objects.filter(
            Q(published=True), 
            reduce(operator.and_, (Q(name__icontains=x) for x in query)) |
            Q(tags__in=talk_tags)
            ).distinct()

    events = Engagement.objects.filter(
            reduce(operator.and_, (Q(event_name__icontains=x) for x in query)) |
            reduce(operator.and_, (Q(location__name__icontains=x) for x in query))
            ).distinct()

    events = events_from_engagements(events)

    speakers = SpkrbarUser.objects.filter(
            reduce(operator.and_, (Q(full_name__icontains=x) for x in query)) |
            Q(tags__in=user_tags)
            ).distinct()

    if talks.count() > 12:
        talks = random.sample(talks, 12)

    if len(events) > 12:
        events = random.sample(events, 12)

    if speakers.count() > 12:
        speakers = random.sample(speakers, 12)

    return {'talks': talks,
            'events': events,
            'speakers': speakers}
