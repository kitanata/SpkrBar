import random
from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.db.models import Q

from guardian.shortcuts import assign

from events.models import Event
from locations.models import Location
from locations.forms import LocationForm
from core.models import UserProfile, TalkEvent

from .models import Talk, TalkTag, TalkComment
from .forms import TalkForm
from .helpers import group_talk_events_by_date

@login_required
def talk_new(request):
    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, request.FILES)
        location_form = None

        if talk_form.is_valid():
            talk = Talk()
            talk.name = talk_form.cleaned_data['name']
            talk.abstract = talk_form.cleaned_data['abstract']
            talk.speaker = request.user.get_profile()

            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                with open('talks/static/img/photo/' + photo.name, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                talk.photo = photo.name

            talk.save()
            assign('change_talk', request.user, talk)
            assign('delete_talk', request.user, talk)

            return redirect('/talk/' + str(talk.id))

   
@login_required
def talk_edit(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

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
        'talk': talk,
        'talk_form': talk_form,
        'location_form': location_form
        }, context_instance=RequestContext(request))


@login_required
def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('delete_talk', talk):
        return HttpResponseForbidden()

    for event in talk.event_set.all():
        event.delete()

    talk.delete()

    return redirect('/speaker/' + request.user.username)


@login_required
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


@login_required
def talk_archive(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    talk.published = False
    talk.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


@login_required
def talk_publish(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    talk.published = True
    talk.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    talk_events = TalkEvent.objects.filter(talk=talk)
    events = [ev.event for ev in talk_events]
    attendees = UserProfile.objects.filter(events_attending__in=events)

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__gt=datetime.today())

    user_attending = False
    user_endorsed = False
    will_have_links = False

    if request.user.is_anonymous():
        attendees = attendees.filter(Q(published=True))
    else:
        user_attending = (request.user.get_profile() in attendees)
        user_endorsed = (request.user.get_profile() in talk.endorsements.all())
        attendees = attendees.filter(Q(published=True) | Q(user=request.user))

        will_have_links = (request.user.get_profile() == talk.speaker)

    if not user_attending or not user_endorsed:
        will_have_links = True

    return render_to_response('talk_detail.html', {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'upcoming': upcoming,
        'past': past,
        'attendees': attendees,
        'user_attending': user_attending,
        'user_endorsed': user_endorsed,
        'will_have_links': will_have_links,
        }, context_instance=RequestContext(request))


def talk_comment_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if talk.speaker == request.user.get_profile():
        return redirect('/talk/' + talk_id)

    if request.method == "POST":
        anon = get_object_or_404(UserProfile, user__username="anonymous")

        if request.user.is_anonymous():
            comment = TalkComment(
                    talk=talk,
                    reviewer=anon,
                    comment= request.POST['comment'])
        else:
            comment = TalkComment(
                    talk=talk,
                    reviewer=request.user.get_profile(),
                    comment= request.POST['comment'])

        comment.save()


    return redirect('/talk/' + talk_id)


def talk_endorsement_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    
    talk.endorsements.add(request.user.get_profile())
    talk.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


