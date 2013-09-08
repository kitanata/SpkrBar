from datetime import datetime, timedelta

from django.db.models import Q

from core.helpers import template

from events.models import Event

@template('events/event_list.haml')
def event_list(request):
    events = Event.objects.all().order_by('-year', '-updated_at')

    return {'events': events}
