from datetime import datetime

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.http import HttpResponseNotFound

from core.models import SpkrbarUser
from core.helpers import render_to

from talks.models import Talk

from events.models import Event

from engagements.models import Engagement

from core.forms import ProfileLinkForm, ProfileTagForm, ProfilePhotoForm
from core.forms import EventEditProfileForm, EditProfileForm


def profile_detail(request, username):
    profile = get_object_or_404(SpkrbarUser, username=username)
    talks = Talk.objects.filter(speaker=profile)

    if profile != request.user:
        talks = talks.filter(published=True)
    else:
        link_form = ProfileLinkForm()
        tag_form = ProfileTagForm()
        photo_form = ProfilePhotoForm()
        edit_form = EditProfileForm({
            'name':profile.get_full_name(),
            'about_me':profile.about_me
        })

    engagements = Engagement.objects.filter(
            talk__speaker=profile,
            talk__published=True)

    events = []
    [events.append(te.event) for te in engagements if te.event not in events]

    upcoming = engagements.filter(date__gt=datetime.today())
    past = engagements.filter(date__lt=datetime.today())

    if request.user.is_anonymous():
        following = profile.following.all()
        followers = profile.followers.all()
    else:
        following = profile.following.all()
        followers = profile.followers.all()

    template = 'profile/speaker/detail.haml'
    context = {
        'profile': profile,
        'upcoming': upcoming,
        'past': past,
        'talks': talks,
        'events': events,
        'following': following,
        'followers': followers,
        'last': '/profile/' + username
        }

    if profile == request.user:
        template = 'profile/speaker/detail_user.haml'
        user_context = {
            'link_form': link_form,
            'tag_form': tag_form,
            'photo_form': photo_form,
            'edit_form': edit_form
            }

        context = dict(context.items() + user_context.items())

    return render_to(request, template, context=context)
