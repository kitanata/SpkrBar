from datetime import datetime

from django.shortcuts import get_object_or_404

from django.db.models import Q

from core.models import SpeakerProfile
from core.helpers import render_to

from talks.models import Talk

from events.models import Event

from talkevents.models import TalkEvent

def speaker_detail(request, username):
    speaker = get_object_or_404(SpeakerProfile, user__username=username)

    talks = Talk.objects.filter(speaker=speaker)
    events = Event.objects.filter(owner=speaker)

    if speaker != request.user:
        talks = talks.filter(published=True)

    talk_events = TalkEvent.objects.filter(
            talk__speaker=speaker,
            talk__published=True)

    current = talk_events.filter(
            event__start_date__lt=datetime.today(),
            event__end_date__gt=datetime.today())

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__lt=datetime.today())

    if request.user.is_anonymous():
        following = speaker.following.all()
        followers = speaker.followers.all()
        attending = None
        attended = None
    else:
        following = speaker.following.all()
        followers = speaker.followers.all()

        attendance = speaker.talkevent_set
        attending = attendance.filter(date__gt=datetime.today()).order_by('date')
        attended = attendance.filter(date__lt=datetime.today()).order_by('-date')

    template = 'profile/speaker_profile.haml'

    if request.user == speaker:
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
