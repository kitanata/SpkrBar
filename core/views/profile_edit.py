from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from core.forms import EditProfileForm, EventEditProfileForm

@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            names = form.cleaned_data['name'].split(' ')
            first_name = names[0]
            last_name = ' '.join(names[1:])

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.about_me = form.cleaned_data['about_me']
            request.user.save()

            return redirect(profile.get_absolute_url())

    else:
        return HttpResponseNotFound()
