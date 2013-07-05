from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from core.models import ProfileTag

from core.forms import ProfileTagForm

@login_required
def profile_tag_new(request):
    if request.method == "POST":
        form = ProfileTagForm(request.POST)

        if form.is_valid():
            profile = request.user.get_profile()

            tag_name = form.cleaned_data['name']

            try:
                tag_model = ProfileTag.objects.get(name=tag_name)
            except ObjectDoesNotExist as e:
                tag_model = ProfileTag(name=tag_name)
                tag_model.save()

            profile.tags.add(tag_model)
            profile.save()

            return redirect(request.user.get_absolute_url())
    else:
        return HttpResponseNotFound()
