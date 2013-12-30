import json
from datetime import datetime, timedelta

from core.helpers import template, events_from_engagements
from engagements.models import Engagement

@template('events/event_list.haml')
def event_list(request):
    engagements = Engagement.objects.all()

    events = events_from_engagements(engagements)

    return {
        'events': json.dumps(events)
    }
