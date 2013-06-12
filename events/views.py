# Create your views here.
import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign

from talks.models import Talk
from locations.models import Location
from locations.forms import LocationForm
from core.models import TalkEvent
from core.helpers import render_to

from models import Event
from .helpers import group_events_by_date

@login_required
def event_new(request):
    if request.method == "POST":
        event = Event()
        event.name = request.POST['name']
        event.description = request.POST['description']
        event.owner = request.user.get_profile()
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

        return render_to(request, 'event_new.haml', context=context)


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

        return render_to(request, 'event_edit.haml', context=context)


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

    profile = request.user.get_profile()

    if profile in event.attendees.all():
        event.attendees.remove(profile)
        event.save()
    else:
        event.attendees.add(profile)
        event.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect(event)


def event_list(request):
    published = Q(published=True, owner__published=True)

    if request.user.is_anonymous():
        events = Event.objects.filter(published)
    else:
        events = Event.objects.filter(
                published | Q(owner=request.user.get_profile()))

    group_defs = [ 
            ('-', 30, "Recent Events"), 
            ('+', 14, "Upcoming Events"), 
            ('+', 90, "In the next 3 months"),
            ('+', 270, "In the next year")]

    groups = []
    end_date = datetime.today()
    for group in group_defs:
        if group[0] == '-':
            start_date = datetime.today() - timedelta(days=group[1])
            end_date = datetime.today()
        else:
            start_date = end_date
            end_date = start_date + timedelta(days=group[1])

        result = events.filter(start_date__gt=start_date,
                start_date__lt=end_date)

        if len(result) > 9:
            result = random.sample(result, 8)

        result = list(result)
        result.sort(key=lambda x: x.start_date)

        groups.append((group[2], result))

    return render_to(request, 'event_list.haml', context={'event_groups': groups})


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
    current = talk_events.filter(date__gt=yesterday, date__lt=tomorrow).order_by('date')
    upcoming = talk_events.filter(date__gt=tomorrow).order_by('date')
    recent = talk_events.filter(
            date__gt=(yesterday - timedelta(days=14)), date__lt=yesterday
                ).order_by('-date')

    user_talks = request.user.get_profile().talk_set.all

    context = {
        'event': event,
        'attendees': attendees,
        'user_attending': user_attending,
        'user_talks': user_talks,
        'will_have_links': will_have_links,
        'querystring': event.location.geocode_querystring(),
        'city_querystring': event.location.geocode_city_querystring(),
        'current': current,
        'upcoming': upcoming,
        'recent': recent,
        'last': event.get_absolute_url()
        }

    return render_to(request, 'event_detail.haml', context=context)
