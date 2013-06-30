from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from core.helpers import save_photo_with_uuid

from talks.models import Talk, TalkPhoto
from talks.forms import TalkPhotoForm

@login_required
def talk_photo_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkPhotoForm(request.FILES)

        if form.is_valid():
            if 'photo' in request.FILES:
                photo = request.FILES['photo']

                talk_photo = TalkPhoto()
                talk_photo.photo = save_photo_with_uuid(photo)
                talk_photo.talk = talk
                talk_photo.save()

            return redirect(talk)

    return HttpResponseNotFound()
