from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from core.models import SpeakerLink

from core.forms import ProfileLinkForm

@login_required
def profile_link_new(request):
    if request.method == "POST":
        form = ProfileLinkForm(request.POST)

        if form.is_valid():
            profile = request.user

            link_model = UserLink()

            link_model.type_name = form.cleaned_data['type']
            link_model.url_target = form.cleaned_data['url']
            link_model.profile = profile

            link_model.save()

            return redirect('/profile/edit/')
    return profile_form_view(request)
