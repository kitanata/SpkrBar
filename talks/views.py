import random
from datetime import datetime
from itertools import groupby

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from django.db.models import Q

from guardian.shortcuts import assign

from events.models import Event
from locations.models import Location
from locations.forms import LocationForm
from core.models import UserProfile, TalkEvent
from core.helpers import save_photo_with_uuid

from .models import *
from .forms import *

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
        form = TalkForm(request.POST, instance=talk)

        if form.is_valid():
            form.save()

            return redirect(talk)
    else:
        return HttpResponseNotFound()


@login_required
def talk_link_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkLinkForm(request.POST)

        if form.is_valid():
            link = TalkLink()
            link.name = form.cleaned_data['name']
            link.url = form.cleaned_data['url']
            link.talk = talk
            link.save()

            return redirect(talk)
    else:
        return HttpResponseNotFound()


@login_required
def talk_slides_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkSlideDeckForm(request.POST)

        if form.is_valid():
            deck = TalkSlideDeck()
            deck.talk = talk

            embed = form.cleaned_data['embed']
            embed = embed.split(' ')
            embed = [x.split('=') for x in embed]
            embed = [x for x in embed if len(x) == 2]
            embed = {x[0]: x[1].strip(""" "'""") for x in embed}

            deck.source = form.cleaned_data['source']

            if deck.source == SLIDESHARE:
                deck.data = embed['src']
                w = embed['width']
                h = embed['height']
                deck.aspect = int(w) / float(h) if float(h) != 0 else 0
            elif deck.source == SPEAKERDECK:
                deck.data = embed['data-id']
                deck.aspect = float(embed['data-ratio'])
            else:
                return HttpResponseNotFound()

            deck.save()

            return redirect(talk)

    return HttpResponseNotFound()


@login_required
def talk_video_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkVideoForm(request.POST)

        if form.is_valid():
            video = TalkVideo()
            video.talk = talk

            embed = form.cleaned_data['embed']
            embed = embed.split(' ')
            embed = [x.split('=') for x in embed]
            embed = [x for x in embed if len(x) == 2]
            embed = {x[0]: x[1].strip(""" "'""") for x in embed}

            video.source = form.cleaned_data['source']

            if video.source == YOUTUBE or video.source == VIMEO:
                video.data = embed['src']
                w = embed['width']
                h = embed['height']
                video.aspect = int(w) / float(h) if float(h) != 0 else 0
            else:
                return HttpResponseNotFound()

            video.save()

            return redirect(talk)

    return HttpResponseNotFound()


@login_required
def talk_photo_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkPhotoForm(request.FILES)

        if form.is_valid():
            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                talk_photo = TalkPhoto()
                talk_photo.photo = save_photo_with_uuid(photo)
                talk_photo.talk = talk
                talk_photo.save()

            return redirect(talk)

    return HttpResponseNotFound()


@login_required
def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('delete_talk', talk):
        return HttpResponseForbidden()

    talk.delete()

    return redirect(request.user.get_profile())


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

    talk_events = talk.talkevent_set.all()
    attendees = UserProfile.objects.filter(talkevent__in=talk_events).distinct()

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__gt=datetime.today())

    user_attendance = False
    user_endorsed = False
    will_have_links = False

    if request.user.is_anonymous():
        attendees = attendees.filter(Q(published=True))
    else:
        try:
            user_attendance = talk_events.get(attendees__in=[request.user.get_profile()])
        except ObjectDoesNotExist:
            pass

        user_endorsed = (request.user.get_profile() in talk.endorsements.all())
        attendees = attendees.filter(Q(published=True) | Q(user=request.user))

        will_have_links = (request.user.get_profile() == talk.speaker)

    if user_attendance and not user_endorsed:
        will_have_links = True

    photos = talk.talkphoto_set.all()

    photo_col = []
    for photo in photos:
        width = photo.width
        height = photo.height
        aspect = width / height if height != 0 else 0
        width = min(width, 200)
        photo_col.append((photo.photo, width, width * aspect))

    return render_to_response('talk_detail.haml', {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'photos': photo_col,
        'upcoming': upcoming,
        'past': past,
        'attendees': attendees,
        'user_attendance': user_attendance,
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
