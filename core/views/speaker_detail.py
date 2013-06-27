from datetime import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.db.models import Q

from core.helpers import render_to

from talks.models import Talk

from events.models import Event

from talkevents.models import TalkEvent

def speaker_detail(request, username):
    speaker = get_object_or_404(User, username=username).get_profile()

    talks = Talk.objects.filter(speaker=speaker)
    events = Event.objects.filter(owner=speaker)

    if speaker.user != request.user:
        talks = talks.filter(published=True, speaker__published=True)

    talk_events = TalkEvent.objects.filter(
            talk__speaker=speaker,
            talk__published=True,
            event__owner__published=True,
            talk__speaker__published=True)

    current = talk_events.filter(
            event__start_date__lt=datetime.today(),
            event__end_date__gt=datetime.today())

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__lt=datetime.today())

    if request.user.is_anonymous():
        following = speaker.following.filter(published=True)
        followers = speaker.followers.filter(published=True)
        attending = None
        attended = None
    else:
        following = speaker.following.filter(Q(published=True) | Q(user=request.user))
        followers = speaker.followers.filter(Q(published=True) | Q(user=request.user))

        attendance = speaker.talkevent_set
        attending = attendance.filter(date__gt=datetime.today()).order_by('date')
        attended = attendance.filter(date__lt=datetime.today()).order_by('-date')

    template = 'profile/speaker_profile.haml'

    if request.user == speaker.user:
        template = 'profile/user_profile.haml'

    context = {
        'speaker': speaker,
        'current': current,
        'upcoming': upcoming,
        'past': past,
        'talks': talks,
        'events': events,
        'attending': attending,
        'attended': attended,
        'following': following,
        'followers': followers,
        'last': '/speaker/' + username
        }

    return render_to(request, template, context=context)
