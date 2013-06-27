from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from events.models import Event

@login_required
def event_attendee_new(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    profile = request.user

    if profile in event.attendees.all():
        event.attendees.remove(profile)
        event.save()
    else:
        event.attendees.add(profile)
        event.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect(event)
