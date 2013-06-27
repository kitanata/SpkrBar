from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from events.models import Event

@login_required
def event_close(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.owner != request.user:
        return HttpResponseForbidden()

    event.accept_submissions = False
    event.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect(event)
