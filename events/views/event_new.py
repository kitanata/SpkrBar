import json
from datetime import datetime, date, time

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign

from locations.models import Location
from locations.forms import LocationForm
from core.helpers import render_to

from events.models import Event

@login_required
def event_new(request):
    if request.method == "POST":
        event = Event()
        event.name = request.POST['name']

        sdt = request.POST['start-date'] + request.POST['start-time']
        edt = request.POST['end-date'] + request.POST['end-time']

        event.start_date = datetime.strptime(sdt, "%m/%d/%Y%I:%M %p")
        event.end_date = datetime.strptime(edt, "%m/%d/%Y%I:%M %p")

        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        assign('change_event', request.user, event)
        assign('delete_event', request.user, event)

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        context = {
            'location_form': location_form,
            'locations': locations
            }

        return render_to(request, 'events/event_new.haml', context=context)
