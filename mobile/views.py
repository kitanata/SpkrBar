# Create your views here.
from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from events.models import Event
from events.helpers import group_events_by_date

def index(request):
    if request.user.is_anonymous():
        events = Event.published_events()
    else:
        events = Event.published_events(user_profile=request.user.get_profile())

    events = events.filter(date__gt=datetime.today()).order_by('date')[:20]

    event_groups = group_events_by_date(events)

    return render_to_response('mobile/index.html', {
        'event_groups': event_groups
        }, context_instance=RequestContext(request))


def login(request):
    return render_to_response('mobile/login.html',
            context_instance=RequestContext(request))

def register(request):
    return render_to_response('mobile/register.html',
            context_instance=RequestContext(request))

def event_detail(request):
    return render_to_response('mobile/event-detail.html',
            context_instance=RequestContext(request))

def search(request):
    return render_to_response('mobile/search.html',
            context_instance=RequestContext(request))

def speakers(request):
    return render_to_response('mobile/speakers.html',
            context_instance=RequestContext(request))

def profile(request):
    return render_to_response('mobile/profile.html',
            context_instance=RequestContext(request))
