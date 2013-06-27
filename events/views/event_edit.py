import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from locations.models import Location
from locations.forms import LocationForm
from core.helpers import render_to

from events.models import Event

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if not request.user.has_perm('change_event', event):
        return HttpResponseForbidden()

    if request.method == "POST":
        event.name = request.POST['name']
        event.description = request.POST['description']
        event.owner = request.user.get_profile()
        event.start_date = datetime.strptime(request.POST['start-date'], "%Y-%m-%d %H:%M")
        event.end_date = datetime.strptime(request.POST['end-date'], "%Y-%m-%d %H:%M")
        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        start_date = event.start_date.strftime("%Y-%m-%d %H:%M")
        end_date = event.end_date.strftime("%Y-%m-%d %H:%M")

        context = {
            'event': event,
            'start_date': start_date,
            'end_date': end_date,
            'location_form': location_form,
            'locations': locations
            }

        return render_to(request, 'events/event_edit.haml', context=context)
