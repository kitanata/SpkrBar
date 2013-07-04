from datetime import datetime

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.http import HttpResponseNotFound

from core.models import SpkrbarUser
from core.helpers import render_to

from talks.models import Talk

from events.models import Event

from talkevents.models import TalkEvent

from core.forms import ProfileLinkForm, ProfileTagForm, ProfilePhotoForm, EditProfileForm


def speaker_profile(profile, user):
    talks = Talk.objects.filter(speaker=profile)

    if profile.user != user:
        talks = talks.filter(published=True)
    else:
        link_form = ProfileLinkForm()
        tag_form = ProfileTagForm()
        photo_form = ProfilePhotoForm()
        edit_form = EditProfileForm({
            'name':profile.user.get_full_name(),
            'about_me':profile.about_me
        })

    talk_events = TalkEvent.objects.filter(
            talk__speaker=profile,
            talk__published=True)

    events = []
    [events.append(te.event) for te in talk_events if te.event not in events]

    current = talk_events.filter(
            event__start_date__lt=datetime.today(),
            event__end_date__gt=datetime.today())

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__lt=datetime.today())

    if profile.user.is_anonymous():
        following = profile.user.following.all()
        followers = profile.user.followers.all()
        attending = None
        attended = None
    else:
        following = profile.user.following.all()
        followers = profile.user.followers.all()

        attending = profile.user.attending.filter(date__gt=datetime.today()).order_by('date')
        attended = profile.user.attending.filter(date__lt=datetime.today()).order_by('-date')

    context = {
        'profile': profile,
        'current': current,
        'upcoming': upcoming,
        'past': past,
        'talks': talks,
        'events': events,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        }

    if profile.user == user:
        user_context = {
            'link_form': link_form,
            'tag_form': tag_form,
            'photo_form': photo_form,
            'edit_form': edit_form
            }

        context = dict(context.items() + user_context.items())

    return context



def attendee_profile(profile, user):
    if profile.user == user:
        tag_form = ProfileTagForm()
        photo_form = ProfilePhotoForm()
        edit_form = EditProfileForm({
            'name':profile.user.get_full_name(),
            'about_me':profile.about_me
        })

    endorsed = profile.user.talks_endorsed.all()

    if profile.user.is_anonymous():
        following = profile.user.following.all()
        followers = profile.user.followers.all()
        attending = None
        attended = None
    else:
        following = profile.user.following.all()
        followers = profile.user.followers.all()

        attendance = profile.user.attending
        attending = attendance.filter(date__gt=datetime.today()).order_by('date')
        attended = attendance.filter(date__lt=datetime.today()).order_by('-date')

    context = {
        'profile': profile,
        'endorsed': endorsed,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        }

    if profile.user == user:
        user_context = {
            'tag_form': tag_form,
            'photo_form': photo_form,
            'edit_form': edit_form
            }

        context = dict(context.items() + user_context.items())

    return context


def event_profile(profile, user):
    events = Event.objects.filter(owner=profile)

    talk_events = TalkEvent.objects.filter(
            talk__speaker=profile,
            talk__published=True)

    current = talk_events.filter(
            event__start_date__lt=datetime.today(),
            event__end_date__gt=datetime.today())

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__lt=datetime.today())

    if profile.user.is_anonymous():
        following = profile.user.following.all()
        followers = profile.user.followers.all()
        attending = None
        attended = None
    else:
        following = profile.user.following.all()
        followers = profile.user.followers.all()

        attendance = profile.user.attending
        attending = attendance.filter(date__gt=datetime.today()).order_by('date')
        attended = attendance.filter(date__lt=datetime.today()).order_by('-date')

    return {
        'profile': profile,
        'current': current,
        'upcoming': upcoming,
        'past': past,
        'events': events,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        }


def profile_detail(request, username):
    profile = get_object_or_404(SpkrbarUser, username=username).get_profile()

    profile_types = {
        SpkrbarUser.USER_TYPE_SPEAKER: speaker_profile,
        SpkrbarUser.USER_TYPE_ATTENDEE: attendee_profile,
        SpkrbarUser.USER_TYPE_EVENT: event_profile }

    user_templates = {
        SpkrbarUser.USER_TYPE_SPEAKER: 'profile/speaker/detail_user.haml',
        SpkrbarUser.USER_TYPE_ATTENDEE: 'profile/attendee/detail_user.haml',
        SpkrbarUser.USER_TYPE_EVENT: 'profile/event/detail_user.haml' }

    profile_templates = {
        SpkrbarUser.USER_TYPE_SPEAKER: 'profile/speaker/detail.haml',
        SpkrbarUser.USER_TYPE_ATTENDEE: 'profile/attendee/detail.haml',
        SpkrbarUser.USER_TYPE_EVENT: 'profile/event/detail.haml' }

    try:
        context = profile_types[profile.user.user_type](profile, request.user)
        context['last'] = '/profile/' + username

        print "HELLO"
        
        if request.user == profile.user:
            template = user_templates[profile.user.user_type]
        else:
            template = profile_templates[profile.user.user_type]

        print template

        return render_to(request, template, context=context)
    except Exception as e:
        print str(e)
        return HttpResponseNotFound()
