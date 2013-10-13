from datetime import datetime, timedelta

from core.helpers import template, events_from_engagements
from engagements.models import Engagement

@template('event_list.haml')
def event_list(request):
    start_date = datetime.today() - timedelta(days=14)
    end_date = datetime.today() + timedelta(days=14)

    engagements = Engagement.objects.filter(
        date__gte=start_date.date(), date__lt=end_date.date())

    events = events_from_engagements(engagements)

    return {
        'events': events
    }
