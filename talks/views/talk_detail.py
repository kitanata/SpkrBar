from datetime import datetime

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from core.models import SpkrbarUser
from core.helpers import template

from talks.models import Talk
from talks.forms import TalkLinkForm
from engagements.forms import RatingForm

@template('talks/talk_base.haml')
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    rating_form = RatingForm()
    link_form = TalkLinkForm()

    return {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'rating_form': rating_form,
        'link_form': link_form,
        }
