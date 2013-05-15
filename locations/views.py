# Create your views here.
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.db.models import Q

from models import Location
from forms import LocationForm

def locations(request):
    locations = Location.objects.all()

    return render_to_response('locations.html', {
        'locations': locations,
        }, context_instance=RequestContext(request))


def location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    events = location.event_set

    if not request.user.is_anonymous():
        events = events.filter(
                Q(talk__published=True, talk__speaker__published=True) | Q(talk__speaker=request.user.get_profile()))

    upcoming = events.filter(date__gt=datetime.now()).order_by('date')[:5]
    past = events.filter(date__lt=datetime.now()).order_by('-date')[:20]

    return render_to_response('location.html', {
        'location': location,
        'querystring': location.geocode_querystring(),
        'city_querystring': location.geocode_city_querystring(),
        'upcoming': upcoming,
        'past': past,
        }, context_instance=RequestContext(request))


def location_new(request):
    if request.method == 'POST': # If the form has been submitted...
        location_form = LocationForm(request.POST)

        if location_form.is_valid():
            location = location_form.save()
            location.save()

    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        return redirect('/talk/new')
