from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from core.models import SpeakerLink

from core.forms import ProfileLinkForm

@login_required
def profile_link_new(request):
    if request.method == "POST":
        form = ProfileLinkForm(request.POST)

        if form.is_valid():
            profile = request.user.get_profile()

            link_model = SpeakerLink()

            link_model.type_name = form.cleaned_data['type']
            link_model.url_target = form.cleaned_data['url']
            link_model.speaker = profile

            link_model.save()

            return redirect(request.user.get_profile())
    else:
        return HttpResponseNotFound()
