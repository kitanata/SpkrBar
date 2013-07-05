from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from core.helpers import save_photo_with_uuid

from core.forms import ProfilePhotoForm

@login_required()
def profile_edit_photo(request):
    if request.method == "POST":
        form = ProfilePhotoForm(request.FILES)

        if form.is_valid():
            profile = request.user.get_profile()

            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                profile.photo = save_photo_with_uuid(photo)

            profile.save()

            return redirect(request.user)
    else:
        return HttpResponseNotFound()
