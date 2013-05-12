from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from locations.models import Location
from locations.forms import LocationForm
from core.models import UserProfile
from .models import Talk, TalkEvent, TalkTag, TalkComment
from .forms import TalkForm
from .helpers import group_talk_events_by_date

def talk_list(request):

    if request.user.is_anonymous():
        events = TalkEvent.objects.filter(
                talk__speakers__published=True,
                talk__published=True, date__gt=datetime.now()
                ).order_by('date')[:20]
    else:
        events = TalkEvent.objects.filter(
                Q(talk__speakers__published=True) | Q(talk__speakers__in=[request.user.get_profile()]),
                talk__published=True, date__gt=datetime.now()
                ).order_by('date')[:20]

    event_groups = group_talk_events_by_date(events)

    return render_to_response("talk_list.html", {
        'event_groups': event_groups
        }, context_instance=RequestContext(request))


def talk_new(request):

    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, request.FILES)
        location_form = None

        if talk_form.is_valid():
            talk = talk_form.save()
            talk.speakers.add(request.user.get_profile())

            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                with open('talk/static/img/photo/' + photo.name, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                talk.photo = photo.name

            talk.save()

            return redirect('/talk/' + str(talk.id))
    else:
        talk_form = TalkForm()
        location_form = LocationForm()

    return render_to_response('talk_new.html', {
        'talk_form' : talk_form,
        'location_form' : location_form
        }, context_instance=RequestContext(request))

    
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    events = TalkEvent.objects.filter(talk__id=talk_id)
    attendees = UserProfile.objects.filter(events_attending__in=events)

    if request.user.is_anonymous():
        attendees = attendees.filter(Q(published=True))
    else:
        attendees = attendees.filter(Q(published=True) | Q(user=request.user))

    return render_to_response('talk_detail.html', {
        'talk': talk,
        'events': events.filter(date__gt=datetime.now()),
        'attendees': attendees
        }, context_instance=RequestContext(request))


def talk_edit(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, request.FILES, instance=talk)

        if talk_form.is_valid():
            talk = talk_form.save()

            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                with open('talks/static/img/photo/' + photo.name, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                talk.photo = photo.name

            talk.save()

            return redirect('/talk/' + str(talk.id))
    else:
        talk_form = TalkForm(instance=talk)

    location_form = LocationForm()

    return render_to_response('talk_edit.html', {
        'talk_form': talk_form,
        'location_form': location_form
        }, context_instance=RequestContext(request))


def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.delete()

    return redirect('/speaker/' + request.user.username)


def location_new(request):
    if request.method == 'POST': # If the form has been submitted...
        location_form = LocationForm(request.POST)

        if location_form.is_valid():
            location = location_form.save()
            location.save()

    return redirect('/talk/new')


def talk_tag_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        tag = request.POST['tag']

        try:
            tag_obj = TalkTag.objects.get(name=tag)
        except ObjectDoesNotExist as e:
            tag_obj = TalkTag(name=tag)
            tag_obj.save()

        talk.tags.add(tag_obj)

    return redirect('/talk/' + talk_id)


def talk_comment_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if request.method == "POST":
        if request.user.get_profile() not in talk.speakers.all():
            comment = TalkComment(
                    talk=talk,
                    reviewer=request.user.get_profile(),
                    comment = request.POST['comment'])

            comment.save()

    return redirect('/talk/' + talk_id)


def talk_endorsement_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    
    talk.endorsements.add(request.user.get_profile())
    talk.save()

    if 'last' in request.GET:
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


def talk_attendee_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    talk.attendees.add(request.user.get_profile())
    talk.save()

    if 'last' in request.GET:
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


def talk_archive(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.published = False
    talk.save()

    if 'last' in request.GET:
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


def talk_publish(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.published = True
    talk.save()

    if 'last' in request.GET:
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)
