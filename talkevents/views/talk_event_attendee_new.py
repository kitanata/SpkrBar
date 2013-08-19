from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from talkevents.models import TalkEvent

@login_required()
def talk_event_attendee_new(request, talk_event_id):
    talk_event = get_object_or_404(TalkEvent, pk=talk_event_id)

    if request.user in talk_event.attendees.all():
        talk_event.attendees.remove(request.user)
        talk_event.save()
    else:
        talk_event.attendees.add(request.user)
        talk_event.save()

    if 'last' in request.GET and request.GET['last']:
        return redirect(request.GET['last'])
    else:
        return redirect(request.user)
