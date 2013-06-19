from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from forms import EditProfileForm

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
            user.save()

            profile = user.get_profile()
            profile.about_me = form.cleaned_data['about_me']
            profile.save()

            return redirect('/profile/edit/')

    else:
        return profile_form_view(request)
