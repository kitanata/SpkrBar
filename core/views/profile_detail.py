from django.shortcuts import get_object_or_404

from core.helpers import template
from core.models import SpkrbarUser

@template('profile/profile_base.haml')
def profile_detail(request, id):
    profile = get_object_or_404(SpkrbarUser, pk=id)

    return {
        'profile': profile,
        }
