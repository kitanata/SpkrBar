from datetime import datetime

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.http import HttpResponseNotFound

from core.models import SpkrbarUser
from core.helpers import render_to, template

from talks.models import Talk

from engagements.models import Engagement

from core.forms import ProfileLinkForm, ProfileTagForm, ProfilePhotoForm
from core.forms import EventEditProfileForm, EditProfileForm

@template('profile/profile_base.haml')
def profile_detail(request, username):
    profile = get_object_or_404(SpkrbarUser, username=username)

    return {
        'profile': profile,
        }

def profile_detail_old(request, username):
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

    if request.user.is_anonymous():
        following = profile.following.all()
        followers = profile.followers.all()
    else:
        following = profile.following.all()
        followers = profile.followers.all()

    template = 'profile/speaker/detail.haml'
    context = {
        'profile': profile,
        'engagements': engagements,
        'talks': talks,
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
