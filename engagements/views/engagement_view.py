from datetime import datetime, timedelta

from django.db.models import Q

from engagements.models import Engagement
from core.helpers import template

@template('engagements/engagement.haml')
def engagement_view(request, slug):
    slugs = slug.split('-')
    engagements = Engagement.objects.filter(
        reduce(lambda x, y: x & y, [Q(event_name__icontains=x) for x in slugs]),
        )
    past = engagements.filter(
        active=True, date__lt=datetime.today()).order_by('-date', '-time')

    current = engagements.filter(
        active=True, date__gte=datetime.today()).order_by('-date', '-time')

    speakers = set([e.talk.speaker for e in engagements])

    return {
        'current': current,
        'past': past,
        'speakers': speakers,
    }
