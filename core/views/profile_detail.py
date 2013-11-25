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
def profile_detail(request, id):
    profile = get_object_or_404(SpkrbarUser, pk=id)

    return {
        'profile': profile,
        }
