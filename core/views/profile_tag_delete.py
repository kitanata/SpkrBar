from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from core.models import ProfileTag

@login_required
def profile_tag_delete(request, tag_id):
    if request.method == "POST":
        tag = get_object_or_404(ProfileTag, pk=tag_id)
        tag.delete()

        return redirect(request.user.get_absolute_url())
    else:
        return HttpResponseNotFound()
