import json
from datetime import datetime

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
        event.description = request.POST['description']
        event.owner = request.user
        event.start_date = datetime.strptime(request.POST['start-date'], "%Y-%m-%d %H:%M")
        event.end_date = datetime.strptime(request.POST['end-date'], "%Y-%m-%d %H:%M")
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
