# Create your views here.
import json
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign

from talks.models import Talk
from locations.models import Location
from locations.forms import LocationForm

from models import Event
from .helpers import group_events_by_date

@login_required
def event_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        event = Event()
        event.talk = talk
        event.date = datetime.strptime(request.POST['date'], "%Y-%m-%d %H:%M")
        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        assign('change_event', request.user, event)
        assign('delete_event', request.user, event)

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        return render_to_response('event_new.html', {
            'talk': talk,
            'location_form': location_form,
            'locations': locations,
            }, context_instance=RequestContext(request))


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if not request.user.has_perm('change_event', event):
        return HttpResponseForbidden()

    if request.method == "POST":
        event.date = datetime.strptime(request.POST['date'], "%Y-%m-%d %H:%M")
        event.location = get_object_or_404(Location, pk=request.POST['location'])
        event.save()

        return HttpResponse(json.dumps({}), mimetype="application/json")
    else:
        location_form = LocationForm()

        locations = Location.objects.all()

        date = event.date.strftime("%Y-%m-%d %H:%M")

        return render_to_response('event_edit.html', {
            'event': event,
            'date': date,
            'location_form': location_form,
            'locations': locations
            }, context_instance=RequestContext(request))


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if not request.user.has_perm('delete_event', event):
        return HttpResponseForbidden()

    talk = event.talk
    event.delete()

    return redirect(talk)


@login_required
def event_attendee_new(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    event.attendees.add(request.user.get_profile())
    event.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/event/' + event_id)


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

    user_attending = False
    user_endorsed = False
    will_have_links = False

    if request.user.is_anonymous():
        attendees = event.attendees.filter(Q(published=True))
    else:
        attendees = event.attendees.filter(Q(published=True) | Q(user=request.user))
        user_attending = (request.user.get_profile() in attendees)
        user_endorsed = (request.user.get_profile() in event.talk.endorsements.all())

        will_have_links = (request.user.get_profile() == event.talk.speaker)

    if not user_attending or not user_endorsed:
        will_have_links = True

    return render_to_response('event_detail.html', {
        'event': event,
        'attendees': attendees,
        'user_attending': user_attending,
        'user_endorsed': user_endorsed,
        'will_have_links': will_have_links,
        }, context_instance=RequestContext(request))
