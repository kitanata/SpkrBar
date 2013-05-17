from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from events.models import Event
from locations.models import Location
from locations.forms import LocationForm
from core.models import UserProfile


from .models import Talk, TalkTag, TalkComment
from .forms import TalkForm
from .helpers import group_talk_events_by_date

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

    events = Event.objects.filter(talk__id=talk_id)
    attendees = UserProfile.objects.filter(events_attending__in=events)

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
        'events': events.filter(date__gt=datetime.now()),
        'attendees': attendees,
        'user_attending': user_attending,
        'user_endorsed': user_endorsed,
        'will_have_links': will_have_links,
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
        'talk': talk,
        'talk_form': talk_form,
        'location_form': location_form
        }, context_instance=RequestContext(request))


def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.delete()

    return redirect('/speaker/' + request.user.username)


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


def talk_archive(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.published = False
    talk.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)


def talk_publish(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    talk.published = True
    talk.save()

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)
