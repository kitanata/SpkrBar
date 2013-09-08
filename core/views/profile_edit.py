from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from core.forms import EditProfileForm, EventEditProfileForm

@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            user = request.user

            names = form.cleaned_data['name'].split(' ')
            first_name = names[0]
            last_name = ' '.join(names[1:])

            profile = user.get_profile()
            profile.first_name = first_name
            profile.last_name = last_name
            profile.about_me = form.cleaned_data['about_me']
            profile.save()

            return redirect(profile.get_absolute_url())

    else:
        return HttpResponseNotFound()
