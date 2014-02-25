from django.shortcuts import get_object_or_404
from core.helpers import template

from talks.models import Talk
from talks.forms import TalkLinkForm

@template('talks/talk_base.haml')
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    link_form = TalkLinkForm()

    return {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'link_form': link_form,
        'title': talk.name
        }
