# Create your views here.
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Location

def locations(request):
    locations = Location.objects.all()

    return render_to_response('locations.html', {
        'locations': locations,
        }, context_instance=RequestContext(request))

def location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    talks = location.talk_set

    if not request.user.is_anonymous():
        talks = talks.filter(Q(published=True, speakers__published=True) | Q(speakers__in=[request.user.get_profile()]))

    upcoming = talks.filter(date__gt=datetime.now()).order_by('date')[:5]
    past = talks.filter(date__lt=datetime.now()).order_by('-date')[:20]

    return render_to_response('location.html', {
        'location': location,
        'querystring': location.geocode_querystring(),
        'city_querystring': location.geocode_city_querystring(),
        'upcoming': upcoming,
        'past': past,
        }, context_instance=RequestContext(request))
