# Create your views here.
import json
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q

from talks.models import Talk
from locations.models import Location
from locations.forms import LocationForm

from models import Event
from .helpers import group_events_by_date

def event_list(request):
    if request.user.is_anonymous():
        events = Event.published_events()
    else:
        events = Event.published_events(user_profile=request.user.get_profile())

    events = events.filter(date__gt=datetime.now()).order_by('date')[:20]

    event_groups = group_events_by_date(events)

    return render_to_response("event_list.html", {
        'event_groups': event_groups
        }, context_instance=RequestContext(request))


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user.is_anonymous:
        attendees = event.attendees.filter(Q(published=True))
    else:
        attendees = event.attendees.filter(Q(published=True) | Q(user=request.user))

    return render_to_response('event_detail.html', {
        'event': event,
        'attendees': attendees,
        }, context_instance=RequestContext(request))


def event_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        event = Event()
        event.talk = talk
        event.date = datetime.strptime(request.POST['date'], "%Y-%m-%d %H:%M")
        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        return render_to_response('event_new.html', {
            'talk': talk,
            'location_form': location_form,
            'locations': locations,
            }, context_instance=RequestContext(request))
