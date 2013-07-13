from datetime import datetime

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from events.models import Event
from core.models import SpeakerProfile, SpkrbarUser
from core.helpers import template

from talks.models import Talk
from talks.forms import TalkRatingForm

@template('talks/talk_detail.haml')
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    talk_events = talk.talkevent_set.all()
    attendees = SpkrbarUser.objects.filter(attending__in=talk_events).distinct()

    upcoming = talk_events.filter(event__start_date__gt=datetime.today())
    past = talk_events.filter(event__end_date__gt=datetime.today())

    user_attendance = False
    user_endorsed = False
    user_rated = False
    will_have_links = False

    attendees = attendees.filter()

    if not request.user.is_anonymous():
        try:
            user_attendance = talk_events.get(attendees__in=[request.user])
        except ObjectDoesNotExist:
            pass

        user_endorsed = (request.user in talk.endorsements.all())
        user_rated = (request.user in [x.rater for x in talk.ratings.all()])

        will_have_links = True

    photos = talk.talkphoto_set.all()

    photo_col = []
    for photo in photos:
        width = photo.width
        height = photo.height
        aspect = width / height if height != 0 else 0
        width = min(width, 200)
        photo_col.append((photo.photo, width, width * aspect))

    events_accepting_talks = Event.objects.filter(accept_submissions=True)

    rating_form = TalkRatingForm()

    return {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'photos': photo_col,
        'upcoming': upcoming,
        'past': past,
        'attendees': attendees,
        'user_attendance': user_attendance,
        'user_endorsed': user_endorsed,
        'user_rated': user_rated,
        'will_have_links': will_have_links,
        'events_accepting_talks': events_accepting_talks,
        'rating_form': rating_form,
        }
