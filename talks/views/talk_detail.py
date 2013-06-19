from datetime import datetime

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from events.models import Event
from core.models import UserProfile
from core.helpers import render_to

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

        user_events = request.user.get_profile().event_set.all()
        user_endorsed = (request.user.get_profile() in talk.endorsements.all())
        attendees = attendees.filter(Q(published=True) | Q(user=request.user))

        will_have_links = (request.user.get_profile() == talk.speaker)

    will_have_links = not user_attendance or not user_endorsed or user_events

    photos = talk.talkphoto_set.all()

    photo_col = []
    for photo in photos:
        width = photo.width
        height = photo.height
        aspect = width / height if height != 0 else 0
        width = min(width, 200)
        photo_col.append((photo.photo, width, width * aspect))

    events_accepting_talks = Event.objects.filter(accept_submissions=True)

    context = {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'photos': photo_col,
        'upcoming': upcoming,
        'past': past,
        'attendees': attendees,
        'user_events': user_events,
        'user_attendance': user_attendance,
        'user_endorsed': user_endorsed,
        'will_have_links': will_have_links,
        'events_accepting_talks': events_accepting_talks
        }

    return render_to(request, 'talk_detail.haml', context=context)
