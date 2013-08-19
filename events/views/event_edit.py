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

        sdt = request.POST['start-date'] + request.POST['start-time']
        edt = request.POST['end-date'] + request.POST['end-time']

        event.start_date = datetime.strptime(sdt, "%m/%d/%Y%I:%M %p")
        event.end_date = datetime.strptime(edt, "%m/%d/%Y%I:%M %p")

        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        start_date = event.start_date.strftime("%m/%d/%Y")
        start_time = event.start_date.strftime("%H:%M")

        end_date = event.end_date.strftime("%m/%d/%Y")
        end_time = event.end_date.strftime("%H:%M")

        context = {
            'event': event,
            'start_date': start_date,
            'start_time': start_time,
            'end_date': end_date,
            'end_time': end_time,
            'location_form': location_form,
            'locations': locations
            }

        return render_to(request, 'events/event_edit.haml', context=context)
