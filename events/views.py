# Create your views here.
import json
from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign

from talks.models import Talk
from locations.models import Location
from locations.forms import LocationForm
from core.models import TalkEvent

from models import Event
from .helpers import group_events_by_date

@login_required
def event_new(request):
    if request.method == "POST":
        import pdb; pdb.set_trace()
        event = Event()
        event.name = request.POST['name']
        event.description = request.POST['description']
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

        return render_to_response('event_new.html', {
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
    published = Q(published=True, owner__published=True)

    if request.user.is_anonymous():
        events = Event.objects.filter(published)
    else:
        events = Event.objects.filter(
                published | Q(owner=request.user.get_profile()))

    return render_to_response('event_list.html', {
        'events': events
        }, context_instance=RequestContext(request))


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    talk_events = TalkEvent.objects.filter(event=event)

    if request.user.is_anonymous():
        talk_events = talk_events.filter(
                talk__published=True, talk__speaker__published=True)
    else:
        talk_events = talk_events.filter(
                Q(talk__published=True, talk__speaker__published=True) | 
                Q(talk__speaker=request.user.get_profile()))

    user_attending = False

    if request.user.is_anonymous():
        attendees = event.attendees.filter(Q(published=True))
    else:
        attendees = event.attendees.filter(Q(published=True) | Q(user=request.user))
        user_attending = (request.user.get_profile() in attendees)

    will_have_links = not user_attending

    yesterday = datetime.today() - timedelta(days=1)
    tomorrow = datetime.today() + timedelta(days=1)
    current = talk_events.filter(date__gt=yesterday, date__lt=tomorrow)
    upcoming = talk_events.filter(date__gt=tomorrow)
    past = talk_events.filter(date__lt=yesterday)

    return render_to_response('event_detail.html', {
        'event': event,
        'attendees': attendees,
        'user_attending': user_attending,
        'will_have_links': will_have_links,
        'querystring': event.location.geocode_querystring(),
        'city_querystring': event.location.geocode_city_querystring(),
        'current': current,
        'upcoming': upcoming,
        'past': past,
        }, context_instance=RequestContext(request))
