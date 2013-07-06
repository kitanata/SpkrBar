from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from events.models import Event

@login_required
def event_endorsement_new(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    event.endorsements.add(request.user)
    event.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/event/' + event_id)
