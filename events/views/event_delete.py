from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from talks.models import Talk

from models import Event

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if not request.user.has_perm('delete_event', event):
        return HttpResponseForbidden()

    talk = event.talk
    event.delete()

    return redirect(talk)
