from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from core.forms import EditProfileForm

from core.views.profile_form_view import profile_form_view

@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            user = request.user

            names = form.cleaned_data['name'].split(' ')
            first_name = names[0]
            last_name = ' '.join(names[1:])

            user.first_name = first_name
            user.last_name = last_name
            user.about_me = form.cleaned_data['about_me']
            user.save()

            return redirect('/profile/edit/')

    else:
        return profile_form_view(request)
